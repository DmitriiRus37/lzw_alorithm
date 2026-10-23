from bitarray import bitarray
from bitarray.util import ba2int

from lzw_compression import ALPHABET_SIZE, COUNT_BYTES, WIDTH_BYTES


class Decompression:

    def decompress(self, source_path: str, dest_path: str) -> None:
        with open(source_path, "rb") as f:
            data = f.read()
        if len(data) < WIDTH_BYTES + COUNT_BYTES:
            raise ValueError("compressed file is truncated")
        width = int.from_bytes(data[:WIDTH_BYTES], "big")
        count = int.from_bytes(data[WIDTH_BYTES:WIDTH_BYTES + COUNT_BYTES], "big")
        bits = bitarray()
        bits.frombytes(data[WIDTH_BYTES + COUNT_BYTES:])
        if width * count > len(bits):
            raise ValueError("compressed file is truncated")

        codes = [ba2int(bits[i * width:(i + 1) * width]) for i in range(count)]
        with open(dest_path, "w", encoding="utf-8", newline="") as f:
            f.write(self.decode(codes))

    @staticmethod
    def decode(codes: list[int]) -> str:
        if not codes:
            return ""
        symbols = [chr(x) for x in range(ALPHABET_SIZE)]
        prev = symbols[codes[0]]
        out = [prev]
        for code in codes[1:]:
            if code < len(symbols):
                entry = symbols[code]
            elif code == len(symbols):
                entry = prev + prev[0]
            else:
                raise ValueError(f"invalid code {code}")
            symbols.append(prev + entry[0])
            out.append(entry)
            prev = entry
        return "".join(out)
