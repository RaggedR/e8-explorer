# Lessons — e8-explorer

Rules for myself, written after mistakes. Review at session start.

## Debugging / verification

- **When a check comes back blank, treat blank as REAL until proven otherwise.**
  Three screenshots came back pure black. I invented "the display is asleep"
  and kept shipping — the page was actually blank the whole time. Do not
  explain away evidence that contradicts "it works." Blank is a result, not
  noise.
- **Verify the real code path, not a proxy.** A syntax check (`node --check`)
  passes on code that still throws at runtime. When I can't screenshot, run the
  actual script against the real data in a DOM stub and drain a few render
  frames. That caught nothing — because I only did it AFTER the user told me it
  was blank. Do it before claiming "it works."
- **Start render loops AFTER initialising state.** A `requestAnimationFrame`
  loop defined mid-script ran its first `draw()` before `loadGraph()` set the
  data, threw on `undefined.edges`, and the uncaught error halted the whole
  init so nothing rendered. Guard draw with an init check, or start the loop
  last.
- **`open <file>` re-focuses a cached tab; it does not reload.** To force a
  fresh load during iteration, use a cache-busting URL (`?v=N`) or tell the
  user to hard-refresh (Cmd+Shift+R).

## Canvas

- **Canvas silently rejects a CSS custom-property string** passed to
  `strokeStyle`/`fillStyle` (it keeps the previous value — often black →
  invisible on dark). Build an explicit `rgba(...)` string in JS instead of
  handing it `getComputedStyle(...).getPropertyValue('--x')`.

## Math-first discipline (worked well — keep doing)

- **Verify the mathematics before writing UI.** The Python generators assert
  the structure (8×30 rings, 11 valencies against ladder.pdf) and refuse to
  emit data otherwise. This caught the E6 "rings = radius-classes" assumption
  (two E6 rings share a radius; rings are Coxeter ORBITS, not radii).
