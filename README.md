# [console-qr](https://github.com/europanite/console-qr "console-qr")

[![CI](https://github.com/europanite/console-qr/actions/workflows/ci.yml/badge.svg)](https://github.com/europanite/console-qr/actions/workflows/ci.yml)
[![pages-build-deployment](https://github.com/europanite/console-qr/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/europanite/console-qr/actions/workflows/pages/pages-build-deployment)

`console-qr` is a small Python CLI that reads a text file from an argument and prints its contents as a QR code directly in the console.

It is useful when you want to pass a short text value, URL, token, or message from a terminal to a smartphone without creating an image file.

## Features

- Reads a text file path from the command line.
- Preserves the file contents, including the final newline.
- Prints a Unicode block QR code to stdout.
- Supports UTF-8 by default.
- Supports QR error correction levels: `L`, `M`, `Q`, and `H`.
- Includes Docker Compose commands and pytest tests.
- Does not use a Makefile.

## Run with Docker Compose

```bash
docker compose run --rm app
```

Run it with your own file by mounting the current directory and passing the file path:

```bash
docker compose run --rm \
  -v "$PWD:/work:ro" \
  app /work/message.txt
```

Run tests:

```bash
docker compose run --rm tests
```

## Run locally

Create a virtual environment and install the package in editable mode:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Print the example text file as a QR code:

```bash
console-qr examples/hello.txt
```

Use a different encoding:

```bash
console-qr --encoding shift_jis message.txt
```

Use stronger error correction:

```bash
console-qr --error-correction H message.txt
```

Invert the terminal blocks:

```bash
console-qr --invert message.txt
```

## Notes

QR codes have a maximum capacity. This tool is intended for short text, URLs, small JSON snippets, or small configuration values. For long files, compress or host the file elsewhere and encode a URL instead.

The script prints the QR code as text only. It does not create PNG, SVG, or other image files.

