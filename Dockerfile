FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY examples ./examples

RUN pip install --no-cache-dir -e ".[dev]"

ENTRYPOINT ["console-text-qr"]
CMD ["examples/hello.txt"]
