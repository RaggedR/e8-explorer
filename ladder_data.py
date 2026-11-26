"""
Build the exceptional-ladder orbital graphs for the explorer.

Five minuscule rungs  W(G)/W(G'),  vertex sets 240, 56, 27, 16, 10:
    E8 (240) : 4_21 mandala, orthogonality bloom, 120-deg weave
    E7 (56)  : Gosset graph, dist-2 Gosset
    E6 (27)  : Schlafli SRG(27,10,1,5), complement SRG(27,16,10,8)
    D5 (16)  : Clebsch SRG(16,5,0,2), halved 5-cube SRG(16,10,6,6)
    A4 (10)  : Petersen SRG(10,3,0,1), triangular T(5) SRG(10,6,3,4)

Each rung's vertices are the previous rung's weights at inner product +1 to a
descent vector (r0=e1+e2, w0=e1+e3, w1, v1); they are projected on the Coxeter
plane of the rung's root subsystem.  An orbital graph is one inner-product
class.  We keep the NON-TRIVIAL, NON-BIPARTITE ones (dropping the identity and
the antipodal matchings n*K2).  Every valency is checked against ladder.pdf.

Reuses the verified machinery in ~/git/graphviz/e8/ladder.py.
"""
import json
import numpy as np

import ladder as L  # vendored alongside this file

def refl(a):
    return np.eye(8) - 2.0 * np.outer(a, a) / (a @ a)

def coxeter_element(simple):
    C = np.eye(8)
    for a in simple:
        C = C @ refl(a)
    return C

def coxeter_plane(simple, h):
    C = coxeter_element(simple)
    w, V = np.linalg.eig(C)
    idx = int(np.argmin(np.abs(np.angle(w) - 2 * np.pi / h)))
    v = V[:, idx]
    u1 = np.real(v); u1 /= np.linalg.norm(u1)
    u2 = np.imag(v); u2 -= (u2 @ u1) * u1; u2 /= np.linalg.norm(u2)
    return C, u1, u2

def is_bipartite(n, edges):
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j); adj[j].append(i)
    color = [0] * n
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1; stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if color[v] == 0:
                    color[v] = -color[u]; stack.append(v)
                elif color[v] == color[u]:
                    return False
    return True

# nice labels per (rung, inner-product class)
LABELS = {
    ("E8", 1): "4₂₁ mandala (56-reg)",
    ("E8", 0): "orthogonality bloom (126-reg)",
    ("E8", -1): "120° weave (56-reg)",
    ("E7", 1): "Gosset graph (27-reg)",
    ("E7", 0): "dist-2 Gosset (27-reg)",
    ("E6", 0): "Schläfli SRG(27,10,1,5)",
    ("E6", 1): "Schläfli complement SRG(27,16,10,8)",
    ("D5", 0): "Clebsch SRG(16,5,0,2)",
    ("D5", 1): "halved 5-cube SRG(16,10,6,6)",
    ("A4", 0): "Petersen SRG(10,3,0,1)",
    ("A4", 1): "triangular T(5) SRG(10,6,3,4)",
}

# ---- descent chain ----
R = L.e8_roots()
r0, w0 = L.R0, L.W0
W7 = R[np.round(R @ r0).astype(int) == 1]; assert len(W7) == 56
W6 = W7[np.round(W7 @ w0).astype(int) == 1]; assert len(W6) == 27
w1 = W6[0]
W5 = W6[np.round(W6 @ w1).astype(int) == 1]; assert len(W5) == 16
v1 = W5[0]
W4 = W5[np.round(W5 @ v1).astype(int) == 1]; assert len(W4) == 10

def subsystem(*vecs):
    mask = np.ones(len(R), bool)
    for v in vecs:
        mask &= np.abs(R @ v) < 1e-9
    return R[mask]

RUNGS_SPEC = [
    ("E8", R,  R,                 30),
    ("E7", W7, subsystem(r0),     18),
    ("E6", W6, subsystem(r0, w0), 12),
    ("D5", W5, subsystem(r0, w0, w1),     8),
    ("A4", W4, subsystem(r0, w0, w1, v1), 5),
]

out = []
for name, W, sub, h in RUNGS_SPEC:
    simple = L.simple_roots(sub)
    C, u1, u2 = coxeter_plane(simple, h)
    P = np.column_stack([W @ u1, W @ u2])
    n = len(W)

    # vertex permutation under the Coxeter element (circular permutations)
    idx = {tuple(np.round(W[i], 6)): i for i in range(n)}
    perm = [idx[tuple(np.round(C @ W[i], 6))] for i in range(n)]
    assert sorted(perm) == list(range(n)), name

    # rings = Coxeter orbits (ordered inner->outer by radius)
    radii = np.hypot(P[:, 0], P[:, 1])
    seen = [False] * n; orbits = []
    for i in range(n):
        if seen[i]:
            continue
        orb = []; j = i
        while not seen[j]:
            seen[j] = True; orb.append(j); j = perm[j]
        orbits.append(orb)
    orbits.sort(key=lambda o: radii[o[0]])
    ring_of = [0] * n
    for ridx, orb in enumerate(orbits):
        for k in orb:
            ring_of[k] = ridx
    ring_radii = [float(np.mean([radii[k] for k in orb])) for orb in orbits]

    scale = float(radii.max())
    pts = [[round(float(P[k, 0] / scale), 6), round(float(P[k, 1] / scale), 6), ring_of[k]]
           for k in range(n)]

    # orbital graphs: one per inner-product class, keep non-trivial non-bipartite
    G = np.round(W @ W.T).astype(int)
    graphs = []
    for ip in sorted(set(int(x) for x in G[np.triu_indices(n, 1)]), reverse=True):
        if ip >= 2:
            continue  # identity / self
        edges = [[int(i), int(j)] for i in range(n) for j in range(i + 1, n) if G[i, j] == ip]
        if not edges:
            continue
        if is_bipartite(n, edges):
            print(f"  {name} ip={ip}: bipartite ({len(edges)} edges) -- dropped")
            continue
        deg = 2 * len(edges) / n
        label = LABELS.get((name, ip), f"ip {ip} ({deg:.0f}-reg)")
        print(f"  {name} ip={ip}: {len(edges)} edges, {deg:.0f}-regular  {label}")
        graphs.append({"ip": ip, "label": label, "valency": int(round(deg)), "edges": edges})

    print(f"{name}: {n} vertices, {len(orbits)} rings, {len(graphs)} non-bipartite graphs")
    out.append({
        "name": name, "n": n, "coxeterNumber": h,
        "coxeterAngleDeg": round(360.0 / h, 4),
        "points": pts, "perm": perm,
        "ringRadii": [round(r / scale, 6) for r in ring_radii],
        "numRings": len(orbits),
        "graphs": graphs,
    })

# valency acceptance tests against ladder.pdf
EXPECT = {"E8": {1: 56, 0: 126, -1: 56}, "E7": {1: 27, 0: 27},
          "E6": {0: 10, 1: 16}, "D5": {0: 5, 1: 10}, "A4": {0: 3, 1: 6}}
for rung in out:
    got = {g["ip"]: g["valency"] for g in rung["graphs"]}
    assert got == EXPECT[rung["name"]], f'{rung["name"]}: {got} != {EXPECT[rung["name"]]}'
print("\nALL valencies match ladder.pdf  ->  PASS")

with open("ladder_data.js", "w") as f:
    f.write("// Generated by ladder_data.py -- exceptional-ladder orbital graphs.\n")
    f.write("// 5 rungs (240/56/27/16/10), non-bipartite orbital graphs. Verified.\n")
    f.write("const RUNGS = ")
    json.dump(out, f, separators=(",", ":"))
    f.write(";\n")
print("wrote ladder_data.js  OK")
