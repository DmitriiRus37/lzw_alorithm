import math

from bitarray import bitarray

# Initial dictionary: every single character of the Basic Multilingual Plane.
ALPHABET_SIZE = 2**16
# Header layout of a compressed file: 1 byte code width + 4 bytes code count.
WIDTH_BYTES = 1
COUNT_BYTES = 4


class Compression:

    def __init__(self):
        self.table_of_codes = {}
        self.list_of_symbols = []
        self.sequence = []
        self.bits_sequence = bitarray()

    def compress(self, source_path: str, dest_path: str) -> None:
        self.list_of_symbols = [chr(x) for x in range(ALPHABET_SIZE)]
        index = {s: i for i, s in enumerate(self.list_of_symbols)}
        self.sequence = []
        with open(source_path, "r", encoding="utf-8", newline="") as f:
            file_str = f.read()

        for ch in file_str:
            if ord(ch) >= ALPHABET_SIZE:
                raise ValueError(f"character {ch!r} is outside the supported alphabet")

        tmp_str = file_str[:1]
        for ch in file_str[1:]:
            if tmp_str + ch in index:
                tmp_str += ch
            else:
                index[tmp_str + ch] = len(self.list_of_symbols)
                self.list_of_symbols.append(tmp_str + ch)
                self.sequence.append(index[tmp_str])
                tmp_str = ch
        if tmp_str:
            self.sequence.append(index[tmp_str])

        bits_per_symbol = math.ceil(math.log(len(self.list_of_symbols), 2))
        self.table_of_codes = {
            s: format(i, f"0{bits_per_symbol}b") for i, s in enumerate(self.list_of_symbols)
        }

        self.bits_sequence = bitarray()
        self.bits_sequence.frombytes(bits_per_symbol.to_bytes(WIDTH_BYTES, "big"))
        self.bits_sequence.frombytes(len(self.sequence).to_bytes(COUNT_BYTES, "big"))
        for code in self.sequence:
            self.bits_sequence.extend(format(code, f"0{bits_per_symbol}b"))

        with open(dest_path, "wb") as f:
            self.bits_sequence.tofile(f)
