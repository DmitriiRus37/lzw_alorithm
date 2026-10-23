# lzw_alorithm

A small LZW (Lempel-Ziv-Welch) compressor for text files. `lzw_compression.py` builds the dictionary while
reading the input and writes the codes as a packed bit stream (via `bitarray`); `lzw_decompression.py`
rebuilds the dictionary and restores the original text. `main.py` is the command-line entry point.

## Tech stack

Python 3.14; bitarray 3.12; pytest + pytest-cov for tests.

## Build & test

```
uv run --group dev pytest   # tests with line + branch coverage; fails below 90 %
```

## Run

```
uv run main.py <src> <dest>          # compress
uv run main.py decode <src> <dest>   # decompress
```

Without uv: `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`, then `./venv/bin/python main.py ...`.
