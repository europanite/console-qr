FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY console_text_qr ./console_text_qr
COPY tests ./tests
COPY examples ./examples

RUN python -m pip install --no-cache-dir -e ".[dev]"

ENTRYPOINT ["console-qr"]
CMD ["examples/hello.txt"]
