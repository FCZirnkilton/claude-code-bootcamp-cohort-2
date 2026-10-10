---
paths: "dashboard/**/*.{html,js,css}"
---

# Release dashboard conventions

- Vanilla HTML, CSS, and ES modules only. Do not add frameworks, bundlers, CDNs, or npm packages.
- One component per file in `dashboard/components/`. Each component exports a render function that takes data and returns or updates DOM. Components do not call `fetch` directly; all API access goes through `dashboard/api.js`.
- Every data view has four states: loading, empty, error (with a retry action), and populated. Wireframe annotations name these states.
- Insert user-provided text with `textContent`, never `innerHTML`.
- Use semantic HTML: real `<button>` and `<label>` elements, visible focus styles, and `aria-live="polite"` for status changes.
- The layout must work at 375 px, 768 px, and 1280 px widths with no horizontal scrolling.
- The browser console must stay clean: no errors or unhandled promise rejections in the core flow.
- After a UI change, verify it in the browser with Claude in Chrome or the manual browser verification checklist, and attach before and after evidence.
