from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Sequence

import qrcode
from qrcode import constants
from qrcode.exceptions import DataOverflowError

ERROR_CORRECTION_LEVELS = {
    "L": constants.ERROR_CORRECT_L,
    "M": constants.ERROR_CORRECT_M,
    "Q": constants.ERROR_CORRECT_Q,
    "H": constants.ERROR_CORRECT_H,
}


def read_text_file(path: str | Path, encoding: str = "utf-8") -> str:
    """Read the target text file exactly as text.

    The final newline is preserved because it may be meaningful when the QR code
    is decoded later.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"file not found: {file_path}")
    if not file_path.is_file():
        raise IsADirectoryError(f"not a file: {file_path}")
    return file_path.read_text(encoding=encoding)


def make_qr_matrix(
    text: str,
    *,
    border: int = 2,
    error_correction: str = "M",
) -> list[list[bool]]:
    """Convert text into a QR-code matrix."""
    if border < 0:
        raise ValueError("border must be 0 or greater")

    level = ERROR_CORRECTION_LEVELS[error_correction.upper()]
    qr = qrcode.QRCode(
        version=None,
        error_correction=level,
        box_size=1,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    return qr.get_matrix()


def render_matrix(
    matrix: Iterable[Iterable[bool]],
    *,
    dark: str = "██",
    light: str = "  ",
    invert: bool = False,
) -> str:
    """Render a QR-code matrix as a terminal-friendly Unicode string."""
    dark_cell, light_cell = (light, dark) if invert else (dark, light)
    return "\n".join(
        "".join(dark_cell if cell else light_cell for cell in row) for row in matrix
    )


def render_text_as_qr(
    text: str,
    *,
    border: int = 2,
    error_correction: str = "M",
    invert: bool = False,
) -> str:
    """Create a terminal QR code string from text."""
    matrix = make_qr_matrix(text, border=border, error_correction=error_correction)
    return render_matrix(matrix, invert=invert)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="console-qr",
        description="Print the contents of a text file as a QR code in the console.",
    )
    parser.add_argument("file", help="Path to the text file to encode")
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Text encoding used to read the file; default: utf-8",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=2,
        help="QR quiet-zone border size; default: 2",
    )
    parser.add_argument(
        "--error-correction",
        choices=sorted(ERROR_CORRECTION_LEVELS),
        default="M",
        help="QR error correction level: L, M, Q, or H; default: M",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Invert dark and light terminal cells for dark terminal themes.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        text = read_text_file(args.file, encoding=args.encoding)
        output = render_text_as_qr(
            text,
            border=args.border,
            error_correction=args.error_correction,
            invert=args.invert,
        )
    except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except DataOverflowError as exc:
        print(f"error: file content is too large for a QR code: {exc}", file=sys.stderr)
        return 2

    print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
