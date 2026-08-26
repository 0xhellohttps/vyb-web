# vyb-web

Public landing / splash page for **VYB** — tour & artist-operations
infrastructure for independent artists.

Single self-contained `index.html` (all assets inlined, no build step, no
network dependencies). Companion to the iOS demo in `vyb-ios`.

## Develop

Open the file directly, or serve it:

```sh
python3 serve.py              # then open http://localhost:8080
```

`serve.py` resolves extensionless URLs the way GitHub Pages does (`/pulse` →
`pulse.html`). Plain `python3 -m http.server` 404s on every internal nav link,
which makes correct links look broken.

## Deploy

Hosted on **GitHub Pages** from `main` (root). Pushing to `main` redeploys.

- Live URL: `https://0xhellohttps.github.io/vyb-web/` (until a custom domain is set)
- Custom domain: add a `CNAME` file with the domain and configure DNS.
