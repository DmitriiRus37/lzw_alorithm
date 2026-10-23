import os
import sys

from lzw_compression import Compression
from lzw_decompression import Decompression


# TODO add compressing of some files to one compressed_file
def main(argv=None):
    argv = sys.argv if argv is None else argv
    if argv[1] == 'decode':
        source_path = os.path.abspath(argv[2])
        dest_path = os.path.abspath(argv[3])
        Decompression().decompress(source_path, dest_path)
    else:
        source_path = os.path.abspath(argv[1])
        dest_path = os.path.abspath(argv[2])
        Compression().compress(source_path, dest_path)


if __name__ == "__main__":
    main()
