#!/usr/bin/env python3
"""Route the map through clear orthogonal lanes, preserving every causal edge.

Run after moving/adding nodes, before build.py. Explicit ports and waypoints are
saved in map.json so the same geometry is rendered, validated and reviewed.
"""
import bisect
import collections
import heapq
import json
import math
import pathlib

import mapgeo

ROOT = pathlib.Path(__file__).resolve().parent.parent


def simplify(points):
    out = []
    for p in points:
        p = [round(v, 2) for v in p]
        if out and p == out[-1]:
            continue
        while len(out) > 1 and ((out[-2][0] == out[-1][0] == p[0])
                               or (out[-2][1] == out[-1][1] == p[1])):
            out.pop()
        out.append(p)
    return out


def route(data):
    nodes, edges, layout = data['nodes'], data['edges'], data['layout']
    boxes = {k: mapgeo.node_box(data, k) for k in nodes}
    sides, groups, ports = {}, collections.defaultdict(list), {}
    normals = {'right': (1, 0), 'left': (-1, 0), 'top': (0, -1), 'bottom': (0, 1)}
    for e in edges:
        a, b = nodes[e['from']], nodes[e['to']]
        if a['layer'] < b['layer']:
            pair = ('right', 'left')
        elif a['layer'] > b['layer']:
            pair = ('left', 'right')
        else:
            between = [n for n in nodes.values() if n['layer'] == a['layer']
                       and min(a['y'], b['y']) < n['y'] < max(a['y'], b['y'])]
            pair = (('bottom', 'top') if a['y'] < b['y'] else ('top', 'bottom')) if not between else ('left', 'left')
            if between:
                e['route'] = 'side'
        sides[e['id']] = pair
        for end, side in zip(('from', 'to'), pair):
            other = e['to'] if end == 'from' else e['from']
            groups[(e[end], side)].append((nodes[other]['y'], e['id'], end))
    for (nid, side), ends in groups.items():
        x1, y1, x2, y2 = boxes[nid]
        for i, (_, eid, end) in enumerate(sorted(ends)):
            delta = (i - (len(ends) - 1) / 2) * min(10, 44 / max(1, len(ends) - 1))
            ports[(eid, end)] = {'right': (x2, (y1 + y2) / 2 + delta),
                                 'left': (x1, (y1 + y2) / 2 + delta),
                                 'top': ((x1 + x2) / 2 + delta, y1),
                                 'bottom': ((x1 + x2) / 2 + delta, y2)}[side]
    xs = {24, layout['viewBox'][0] - 24}
    lane_candidates = set()
    ys = {layout['headerY'] + 48, layout['viewBox'][1] - 24}
    for x in layout['columns']:
        xs.add(x)
    for left, right in zip(layout['columns'], layout['columns'][1:]):
        lo, hi = left + layout['nodeW'] / 2, right - layout['nodeW'] / 2
        lane_candidates.update(round(lo + (hi - lo) * i / 10) for i in range(1, 10))
    for x1, y1, x2, y2 in boxes.values():
        ys.update((y1 - 14, y2 + 14))
    for (eid, end), p in ports.items():
        side = sides[eid][0 if end == 'from' else 1]
        dx, dy = normals[side]
        xs.add(p[0] + dx * 14)
        ys.add(p[1] + dy * 14)
    for x in sorted(lane_candidates):
        if all(abs(x - existing) >= 6 for existing in xs):
            xs.add(x)
    xs, ys = sorted(xs), sorted(ys)
    obstacles = [mapgeo.node_box(data, nid, 7) for nid in nodes]
    clear = {}

    def neighbors(x, y):
        if (x, y) not in clear:
            p = xs[x], ys[y]
            result = []
            for nx, ny, direction in ((x - 1, y, 1), (x + 1, y, 1), (x, y - 1, 2), (x, y + 1, 2)):
                if not (0 <= nx < len(xs) and 0 <= ny < len(ys)):
                    continue
                q = xs[nx], ys[ny]
                if any(max(min(p[0], q[0]), b[0]) <= min(max(p[0], q[0]), b[2])
                       and max(min(p[1], q[1]), b[1]) <= min(max(p[1], q[1]), b[3]) for b in obstacles):
                    continue
                result.append((nx, ny, direction, math.dist(p, q)))
            clear[x, y] = result
        return clear[x, y]

    used, cross = collections.Counter(), collections.defaultdict(set)
    occupied_segments = []

    def overlaps(p, q):
        axis = 0 if abs(p[1] - q[1]) < .01 else 1
        fixed = p[1-axis]
        lo, hi = sorted((p[axis], q[axis]))
        return any(axis == a and abs(fixed - f) < .01 and min(hi, h) - max(lo, l) > .01
                   for a, f, l, h in occupied_segments)
    def occupancy(points):
        for p, q in zip(points, points[1:]):
            if p[0] == q[0]:
                x = bisect.bisect_left(xs, p[0]); direction = 2
                steps = [(x, y) for y in range(bisect.bisect_left(ys, min(p[1], q[1])), bisect.bisect_left(ys, max(p[1], q[1])))]
                for x, y in steps:
                    used[(x, y, x, y + 1)] += 1
                    cross[x, y].add(direction); cross[x, y + 1].add(direction)
            else:
                y = bisect.bisect_left(ys, p[1]); direction = 1
                steps = [(x, y) for x in range(bisect.bisect_left(xs, min(p[0], q[0])), bisect.bisect_left(xs, max(p[0], q[0])))]
                for x, y in steps:
                    used[(x, y, x + 1, y)] += 1
                    cross[x, y].add(direction); cross[x + 1, y].add(direction)

    for e in sorted(edges, key=lambda e: math.dist(ports[e['id'], 'from'], ports[e['id'], 'to'])):
        start, finish = ports[e['id'], 'from'], ports[e['id'], 'to']
        pair = sides[e['id']]
        if pair in (('top', 'bottom'), ('bottom', 'top')):
            points = [start, finish]
        else:
            exits = [tuple(p[i] + normals[side][i] * 14 for i in (0, 1)) for p, side in zip((start, finish), pair)]
            s, t = [tuple((xs if i == 0 else ys).index(p[i]) for i in (0, 1)) for p in exits]
            xmin, xmax = min(s[0], t[0]), max(s[0], t[0])
            if nodes[e['from']]['layer'] == nodes[e['to']]['layer']:
                xmin = bisect.bisect_left(xs, start[0] - 66)
            queue = [(0, 0, *s, 0)]
            best, previous = {(s[0], s[1], 0): 0}, {}
            last = None
            while queue:
                _, cost, x, y, direction = heapq.heappop(queue)
                state = x, y, direction
                if cost != best.get(state):
                    continue
                if (x, y) == t:
                    last = state; break
                for nx, ny, nd, distance in neighbors(x, y):
                    if not xmin <= nx <= xmax:
                        continue
                    if overlaps((xs[x], ys[y]), (xs[nx], ys[ny])):
                        continue
                    key = (min(x, nx), min(y, ny), max(x, nx), max(y, ny))
                    overlap = used[key] * distance * 2.5
                    crossing = 100 if (3 - nd) in cross[nx, ny] else 0
                    newcost = cost + distance + overlap + crossing + (24 if direction and direction != nd else 0)
                    ns = nx, ny, nd
                    if newcost < best.get(ns, float('inf')):
                        best[ns] = newcost; previous[ns] = state
                        heuristic = abs(xs[nx] - xs[t[0]]) + abs(ys[ny] - ys[t[1]])
                        heapq.heappush(queue, (newcost + heuristic, newcost, *ns))
            if last is None:
                raise ValueError(f"No clear route for {e['id']}")
            path = [last]
            while path[-1] in previous:
                path.append(previous[path[-1]])
            points = simplify([start] + [(xs[x], ys[y]) for x, y, _ in reversed(path)] + [finish])
        e['points'] = points
        occupancy(points[1:-1] if len(points) > 2 else points)
        for p, q in zip(points, points[1:]):
            axis = 0 if abs(p[1] - q[1]) < .01 else 1
            occupied_segments.append((axis, p[1-axis], min(p[axis], q[axis]), max(p[axis], q[axis])))

    # These legacy positions are still validated conservatively, though no sign
    # marker is drawn. Place each in clear space without relaxing V11.
    chosen = []
    for e in edges:
        segments = mapgeo.edge_segments(data, e)
        candidates = []
        for i in range(10, 91):
            fraction = i / 100
            point = mapgeo.point_at_fraction(segments, fraction)
            if any(mapgeo.inside(mapgeo.node_box(data, nid, 10), point) for nid in nodes):
                continue
            distance = min((math.dist(point, other) for other in chosen), default=1000)
            candidates.append((distance - abs(fraction - .5) * 8, fraction, point))
        if not candidates:
            raise ValueError(f"No clear legacy sign position for {e['id']}")
        _, fraction, point = max(candidates)
        e['signAt'] = fraction
        chosen.append(point)
    return data


if __name__ == '__main__':
    path = ROOT / 'data/map.json'
    data = route(json.loads(path.read_text(encoding='utf-8')))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Routed {len(data['edges'])} connections through clear lanes")
