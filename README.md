# Static Site Generator (Boot.dev)

A simple static site generator built in Python as part of the Boot.dev curriculum.

It converts Markdown content into HTML pages using a shared template, copies static assets, and outputs a deployable site for GitHub Pages.

## Features

- Converts Markdown to HTML with support for:
  - headings
  - paragraphs
  - blockquotes
  - ordered and unordered lists
  - code blocks
  - inline bold, italic, code, links, and images
- Generates pages recursively from `content/`
- Preserves directory structure in output
- Uses `template.html` placeholders:
  - `{{ Title }}`
  - `{{ Content }}`
- Supports configurable base paths for local hosting and GitHub Pages
- Copies static assets from `static/` into output directory

## Project Structure

```text
.
├── content/            # Markdown pages
├── docs/               # Generated output (GitHub Pages source)
├── src/                # Generator + parser code
├── static/             # CSS, images, other static assets
├── template.html       # HTML page template
├── build.sh            # Production build script (GitHub Pages base path)
├── main.sh             # Local helper script
└── test.sh             # Unit test runner
```

## Requirements

- Python 3.10+ (works with newer versions too)

## Local Development

Generate site (default base path `/`):

```bash
python3 src/main.py
```

Serve locally from `docs/`:

```bash
cd docs && python3 -m http.server 8888
```

Open:

- `http://localhost:8888`

## Production Build (GitHub Pages)

This project is configured for:

- repository: `static-site-generator-bootdev`
- Pages source: `main` branch, `/docs` folder

Run:

```bash
bash build.sh
```

`build.sh` uses the correct base path:

```bash
python3 src/main.py "/static-site-generator-bootdev/"
```

After building, commit and push so GitHub Pages can deploy from `docs/`.

Live URL:

- `https://abdullahshahad-w.github.io/static-site-generator-bootdev/`

## Testing

Run all unit tests:

```bash
bash test.sh
```

## How it Works

At a high level, `src/main.py`:

1. Reads the optional base path from CLI args (`sys.argv`)
2. Copies `static/` to `docs/`
3. Recursively finds all `.md` files in `content/`
4. Converts each Markdown file to HTML
5. Extracts page title from the first `#` heading
6. Injects title/content into `template.html`
7. Rewrites root-relative `href` and `src` with the chosen base path
8. Writes final `.html` files into matching paths in `docs/`

---

Built with Python and a lot of Tolkien appreciation.
