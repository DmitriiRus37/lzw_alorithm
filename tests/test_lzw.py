import pytest

import main
from lzw_compression import Compression
from lzw_decompression import Decompression

SAMPLES = ["test0.txt", "test1.txt", "test3.txt", "test4.txt", "test6.txt"]


def roundtrip(tmp_path, text):
    src = tmp_path / "in.txt"
    src.write_text(text, encoding="utf-8", newline="")
    Compression().compress(str(src), str(tmp_path / "out.lzw"))
    Decompression().decompress(str(tmp_path / "out.lzw"), str(tmp_path / "back.txt"))
    return (tmp_path / "back.txt").read_text(encoding="utf-8", newline="")


@pytest.mark.parametrize("name", SAMPLES)
def test_sample_files_roundtrip(tmp_path, name):
    text = open(f"test_files/{name}", encoding="utf-8", newline="").read()
    assert roundtrip(tmp_path, text) == text


@pytest.mark.parametrize("text", ["", "a", "ab", "aaaaaaa", "abababab", "TOBEORNOTTOBEORTOBEORNOT",
                                  "привет\r\nмир\n", "é￾中"])
def test_edge_case_roundtrip(tmp_path, text):
    assert roundtrip(tmp_path, text) == text


def test_compress_produces_expected_codes(tmp_path):
    src = tmp_path / "in.txt"
    src.write_text("abababab", encoding="utf-8")
    c = Compression()
    c.compress(str(src), str(tmp_path / "out"))
    base = 2**16
    # a b ab aba b  ->  97 98 ab=base aba=base+2 b=98
    assert c.sequence == [97, 98, base, base + 2, 98]
    assert c.list_of_symbols[base:] == ["ab", "ba", "aba", "abab"]
    assert all(len(code) == 17 for code in c.table_of_codes.values())
    assert c.table_of_codes["ab"] == format(base, "017b")
    data = (tmp_path / "out").read_bytes()
    assert data[0] == 17
    assert int.from_bytes(data[1:5], "big") == 5
    assert len(data) == 5 + (5 * 17 + 7) // 8


def test_repetitive_input_is_smaller(tmp_path):
    src = tmp_path / "in.txt"
    src.write_text("abc" * 5000, encoding="utf-8")
    Compression().compress(str(src), str(tmp_path / "out"))
    assert (tmp_path / "out").stat().st_size < src.stat().st_size / 5


def test_character_outside_alphabet_rejected(tmp_path):
    src = tmp_path / "in.txt"
    src.write_text("hi \U0001F600", encoding="utf-8")
    with pytest.raises(ValueError, match="outside the supported alphabet"):
        Compression().compress(str(src), str(tmp_path / "out"))


def test_decode_kwkwk_case():
    # code == len(symbols) case: "aaa" -> [97, base]
    assert Decompression.decode([97, 2**16]) == "aaa"


def test_decode_invalid_code():
    with pytest.raises(ValueError, match="invalid code"):
        Decompression.decode([97, 2**16 + 5])


@pytest.mark.parametrize("payload", [b"", b"\x11\x00", b"\x11\x00\x00\x00\x05\x00"])
def test_truncated_file_rejected(tmp_path, payload):
    (tmp_path / "bad").write_bytes(payload)
    with pytest.raises(ValueError, match="truncated"):
        Decompression().decompress(str(tmp_path / "bad"), str(tmp_path / "out"))


def test_main_encode_then_decode(tmp_path):
    src = tmp_path / "in.txt"
    src.write_text("hello hello hello", encoding="utf-8")
    main.main(["main.py", str(src), str(tmp_path / "c")])
    main.main(["main.py", "decode", str(tmp_path / "c"), str(tmp_path / "d.txt")])
    assert (tmp_path / "d.txt").read_text(encoding="utf-8") == "hello hello hello"
