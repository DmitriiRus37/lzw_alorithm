import math


class Compression:

    def __init__(self):
        self.table_of_codes = {}
        self.list_of_symbols = []
        self.sequence = []
        self.bits_sequence = bitarray()

    def compress(self, source_path: str, dest_path: str) -> None:
        [self.list_of_symbols.append(chr(x)) for x in range(2**16)]
        with open(source_path, "r") as f:
            file_str = f.read()

            total_str = file_str[:1]
            tmp_str = total_str
            # self.sequence.append(self.list_of_symbols.index(tmp_str))
            for i in range(1, len(file_str)):
                ch = file_str[i]
                if tmp_str+ch in self.list_of_symbols:
                    tmp_str += ch
                else:
                    self.list_of_symbols.append(tmp_str+ch)
                    seq_to_append = tmp_str
                    self.sequence.append(self.list_of_symbols.index(seq_to_append))
                    tmp_str = ch

        bits_per_symbol = math.ceil(math.log(len(self.list_of_symbols), 2))
        for i in range(len(self.list_of_symbols)):
            s = self.list_of_symbols[i]
            code = '{0:b}'.format(i)
            self.table_of_codes[s] = '0' * (bits_per_symbol - len(code)) + code

        with open(dest_path, "wb") as f:
            f.write(self.sequence)

        print()






