from __future__ import annotations

from console_text_qr.cli import main, read_text_file, render_matrix, render_text_as_qr


def test_read_text_file_preserves_trailing_newline(tmp_path):
    text_file = tmp_path / "message.txt"
    text_file.write_text("hello\n", encoding="utf-8")

    assert read_text_file(text_file) == "hello\n"


def test_render_matrix_uses_unicode_blocks():
    matrix = [[True, False], [False, True]]

    assert render_matrix(matrix) == "██  \n  ██"


def test_render_text_as_qr_returns_multiline_string():
    rendered = render_text_as_qr("hello", border=1)

    assert "██" in rendered
    assert len(rendered.splitlines()) > 10


def test_main_prints_qr_code(tmp_path, capsys):
    text_file = tmp_path / "message.txt"
    text_file.write_text("hello from file", encoding="utf-8")

    exit_code = main([str(text_file)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "██" in captured.out
    assert captured.err == ""


def test_main_returns_error_for_missing_file(capsys):
    exit_code = main(["does-not-exist.txt"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "file not found" in captured.err
