# lzw_alorithm

`
python3 -m venv venv && 
chmod +x ./venv/bin/activate && 
./venv/bin/activate && 
./venv/bin/pip install -r requirements.txt
`

Usage: `python main.py <src> <dest>` to compress, `python main.py decode <src> <dest>` to decompress.

Tests (coverage must stay >= 90%): `uv run --group dev pytest`
