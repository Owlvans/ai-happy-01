# The rescue thanks him

This entry features a heartwarming scene in warm golden-hour light, capturing a laughing firefighter in uniform with his eyes crinkled shut while the tiny orange kitten he just rescued, perched on his forearm, affectionately licks his nose.

`main.py` is a Python 3.13 stdlib-only validator and copier script that verifies `happy-1024.jpg` against strict security and format requirements, including cryptographic SHA256 pinning (`1864111374b9a3d22b797fe3f9fbb858c17ea9c438ef241f6188f753b5b9bdc1`), exact byte length checks (210545 bytes), 1024x1024 maximum dimensions, and structural JPEG/PNG validation without third-party dependencies. It copies the verified asset safely to `entry.png` within `MAKEFUN_OUTPUT_DIR` (default `/output`).

To run locally:
```bash
python3 main.py
```
Or with a custom output directory:
```bash
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Note: the image files for this entry are not included in this repository because the upload channel used here is text-only.
