#!/usr/bin/env python3
"""
Entry Contract: ai-happy-01 (v2 resubmission)
Title: The rescue thanks him
Concept: A laughing firefighter in uniform, eyes crinkled shut, while the tiny orange kitten he rescued,
perched on his forearm, licks his nose, in warm golden-hour light.
"""

import os
import sys
import hashlib

ENTRY_TITLE = "The rescue thanks him"
EXPECTED_SHA256 = "1864111374b9a3d22b797fe3f9fbb858c17ea9c438ef241f6188f753b5b9bdc1"
EXPECTED_BYTES = 210545
MAX_BYTES = 1048576
MAX_DIM = 1024

def validate_jpeg(data: bytes):
    if not data.startswith(b'\xff\xd8'):
        raise ValueError("Invalid JPEG: missing SOI marker")
    if not data.endswith(b'\xff\xd9'):
        raise ValueError("Invalid JPEG: missing EOI marker")
    
    i = 2
    width, height = None, None
    while i < len(data) - 1:
        if data[i] != 0xff:
            i += 1
            continue
        while i < len(data) and data[i] == 0xff:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in (0xd8, 0xd9, 0x01) or (0xd0 <= marker <= 0xd7):
            continue
        if i + 2 > len(data):
            raise ValueError("Invalid JPEG: truncated marker length")
        length = int.from_bytes(data[i:i+2], 'big')
        if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
            if i + 7 > len(data):
                raise ValueError("Invalid JPEG: truncated SOF segment")
            height = int.from_bytes(data[i+3:i+5], 'big')
            width = int.from_bytes(data[i+5:i+7], 'big')
            break
        i += length
    
    if width is None or height is None:
        raise ValueError("Invalid JPEG: SOF marker not found")
    return width, height

def validate_png(data: bytes):
    png_sig = b'\x89PNG\r\n\x1a\n'
    if not data.startswith(png_sig):
        raise ValueError("Invalid PNG: signature mismatch")
    if not data.endswith(b'IEND\xaeB`\x82'):
        raise ValueError("Invalid PNG: missing IEND trailer")
    
    i = len(png_sig)
    width, height = None, None
    has_iend = False
    while i < len(data):
        if i + 12 > len(data):
            break
        length = int.from_bytes(data[i:i+4], 'big')
        chunk_type = data[i+4:i+8]
        if chunk_type == b'IHDR':
            if length < 8:
                raise ValueError("Invalid PNG: invalid IHDR length")
            width = int.from_bytes(data[i+8:i+12], 'big')
            height = int.from_bytes(data[i+12:i+16], 'big')
        elif chunk_type == b'IEND':
            has_iend = True
        i = i + 12 + length
    
    if width is None or height is None:
        raise ValueError("Invalid PNG: IHDR chunk not found")
    if not has_iend:
        raise ValueError("Invalid PNG: IEND chunk not found")
    return width, height

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "happy-1024.jpg")

    if not os.path.exists(image_path):
        print(f"Error: Required image asset missing at {image_path}", file=sys.stderr)
        sys.exit(1)

    file_size = os.path.getsize(image_path)
    if file_size > MAX_BYTES:
        print(f"Error: File size {file_size} exceeds MAX_BYTES ({MAX_BYTES})", file=sys.stderr)
        sys.exit(1)

    with open(image_path, "rb") as f:
        data = f.read()

    if len(data) != EXPECTED_BYTES:
        print(f"Error: Byte size mismatch. Expected {EXPECTED_BYTES}, got {len(data)}", file=sys.stderr)
        sys.exit(1)

    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA256:
        print(f"Error: SHA256 mismatch. Expected {EXPECTED_SHA256}, got {sha}", file=sys.stderr)
        sys.exit(1)

    if data.startswith(b'\xff\xd8'):
        width, height = validate_jpeg(data)
    elif data.startswith(b'\x89PNG\r\n\x1a\n'):
        width, height = validate_png(data)
    else:
        print("Error: Unsupported image format (neither JPEG nor PNG)", file=sys.stderr)
        sys.exit(1)

    if width > MAX_DIM or height > MAX_DIM:
        print(f"Error: Dimensions ({width}x{height}) exceed maximum allowed ({MAX_DIM}x{MAX_DIM})", file=sys.stderr)
        sys.exit(1)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.png")

    with open(output_path, "wb") as f:
        f.write(data)

    with open(output_path, "rb") as f:
        out_data = f.read()
    out_sha = hashlib.sha256(out_data).hexdigest()
    if out_sha != sha:
        print(f"Error: Output file SHA256 mismatch! Expected {sha}, got {out_sha}", file=sys.stderr)
        sys.exit(1)
    print("Output verified: written file matches source sha256.")

    print(f"Title: {ENTRY_TITLE} | Dimensions: {width}x{height} | Size: {file_size} bytes | SHA256: {sha}")

if __name__ == "__main__":
    main()
