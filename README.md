# vyb-web

Public landing / splash page for **VYB** — tour & artist-operations
infrastructure for independent artists.

Single self-contained `index.html` (all assets inlined, no build step, no
network dependencies). Companion to the iOS demo in `vyb-ios`.

## Develop

Open the file directly, or serve it:

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## Deploy

Hosted on **GitHub Pages** from `main` (root). Pushing to `main` redeploys.

- Live URL: `https://0xhellohttps.github.io/vyb-web/` (until a custom domain is set)
- Custom domain: add a `CNAME` file with the domain and configure DNS.
