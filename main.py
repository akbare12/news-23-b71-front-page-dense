"""news-23 b71 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error:", msg, file=sys.stderr)
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    if os.path.commonpath([out_dir, HERE]) == HERE:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: %s" % out_dir)
    if not os.path.isfile(SRC):
        fail("entry.png not found next to main.py: %s" % SRC)

    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_SIG:
        fail("entry.png is not a PNG (bad signature)")
    if len(data) < 8 + 25 + 12:
        fail("entry.png is too short to hold IHDR + IEND")
    # IHDR chunk: length 13, type IHDR, then width/height/bit depth/colour type.
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        fail("entry.png has no valid IHDR chunk")
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (1024, 1024):
        fail("entry.png is %dx%d, expected 1024x1024" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        fail("unexpected PNG bit depth %d / colour type %d" % (depth, ctype))
    ihdr_crc_stored, = struct.unpack(">I", data[29:33])
    ihdr_crc = binascii.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF
    if ihdr_crc != ihdr_crc_stored:
        fail("entry.png IHDR CRC mismatch")
    if b"IDAT" not in data:
        fail("entry.png has no IDAT chunk")
    # IEND trailer: last 12 bytes must be length 0, type IEND, CRC.
    iend_len, iend_type = struct.unpack(">I4s", data[-12:-4])
    if iend_len != 0 or iend_type != b"IEND":
        fail("entry.png has no well-formed IEND trailer")

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        fail("output differs from source after copy")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
