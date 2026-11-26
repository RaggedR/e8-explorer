# E8 Explorer

An interactive tour of the **exceptional ladder** — the nested chain of Weyl
groups

```
W(E8) ⊃ W(E7) ⊃ W(E6) ⊃ W(D5) ⊃ W(A4)
```

and the beautiful finite graphs that live on it. Each rung is a minuscule coset
space drawn on its Coxeter plane; each graph is one inner-product class among
the points — which is simultaneously an **orbital graph** and a basis element of
the rung's **Hecke algebra** H(G, H).

**▶ Live:** https://raggedr.github.io/e8-explorer/

## What you can do

- **Pick a rung** (E8 · E7 · E6 · D5 · A4) and one of its graphs. Eleven graphs
  in all, the non-trivial non-bipartite orbitals:
  - **E8** (240 roots): 4₂₁ mandala (56-reg), orthogonality bloom (126-reg), 120° weave (56-reg)
  - **E7** (56 weights): Gosset graph, dist-2 Gosset (both 27-reg)
  - **E6** (27 lines): Schläfli SRG(27,10,1,5) and its complement SRG(27,16,10,8)
  - **D5** (16): Clebsch SRG(16,5,0,2), halved 5-cube SRG(16,10,6,6)
  - **A4** (10): Petersen SRG(10,3,0,1), triangular T(5) SRG(10,6,3,4)
- **Isolate an edge orbit** — the edges are dense, so instead of chasing a thin
  line: **click a vertex** (its edges fatten to amber) → **click one** → its full
  Coxeter-rotation orbit lights up cyan, and the handle vertex drops away.
  Multi-select vertices; click a highlighted edge to drop its orbit.
- **Zoom** by dragging up/down, the wheel, or the +/− buttons — centred on the figure.
- **Pull a ring** — grab any vertex and drag its whole ring in or out, past the
  others, while every vertex keeps its angle (so the rotational symmetry holds).
- **Reset view** returns zoom and every ring to home. Light/dark aware.

## How it's built

Pure static HTML + canvas, no dependencies, no server — `index.html` renders
verified constants from `ladder_data.js`.

`ladder_data.py` generates that data and **refuses to emit it unless it checks
out**: every rung's vertex count, and every graph's valency, is asserted against
the known values (56/126/56, 27/27, the SRG parameters, …) before a byte is
written. The Coxeter-plane projection and root machinery live in the vendored
`ladder.py`.

```bash
python ladder_data.py    # regenerate ladder_data.js (needs numpy); prints the checks
python -m http.server 8000 && open http://localhost:8000   # or just open index.html
```

## The mathematics, in one line

Each graph is a double coset H\G/H: a *graph* to look at and a *Hecke-algebra
basis element* to multiply — the same data, geometric and algebraic. Drop the
bipartite orbitals (the antipodal matchings n·K₂, which are the grading
elements that fold the scheme) and what remains carries the real geometry: the
root polytopes, the 27 lines, and the classical strongly regular graphs
Schläfli, Clebsch and Petersen.

## Licence

MIT © Robin Langer
