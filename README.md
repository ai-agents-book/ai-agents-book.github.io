# aiagentsbook.org

The website for *AI Agents: Designing, Orchestrating, and Governing LLM-Based
Systems* by Michael Bücker and Michael Hewing, to be published by Springer
Nature.

Three hand-written pages — `index.html`, `imprint.html`, `privacy.html` — plus
`style.css`, the cover render, two author portraits, and a favicon. No build
step and no dependencies. Editing the page means editing the HTML; publishing
it means pushing a commit to `main`.

## No external requests

Nothing on these pages is fetched from a third party: the icons are an inline
SVG sprite, the portraits and the cover are local files, and there are no web
fonts, no analytics, and no embedded content. That is what lets the privacy
notice say a visit contacts no one but the host, and it is why there is no
cookie banner. **Keep it that way** — a single `<script src>`, webfont link,
or embedded video would make `privacy.html` false.

The only JavaScript is inline and does one thing: remember whether the visitor
switched the colour scheme. It writes the word `light` or `dark` to local
storage, which `privacy.html` describes.

## Addresses

The site serves at <https://aiagentsbook.org/>. The apex domain is configured
through `CNAME`, with A records at the registrar pointing to GitHub's Pages
addresses; `ai-agents-book.github.io` now redirects here.

The appendices live in [their own repository](https://github.com/ai-agents-book/appendices)
and serve beneath this one at [`/appendices/`](https://aiagentsbook.org/appendices/),
which is the address printed in the book.

## Related

- [ai-agents-book/code](https://github.com/ai-agents-book/code) — runnable code from the book
- [ai-agents-book/appendices](https://github.com/ai-agents-book/appendices) — the book's appendices

## Still to do

- `img/cover-3d.*` is a render of the current cover; replace it if Springer's
  final artwork differs.
- Further endorsements go into the "What readers say" section as they arrive,
  as siblings of the two already there.
