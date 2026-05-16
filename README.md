# dup‑checker

**dup‑checker** is a minimal Python 3 script that detects duplicate lines in a given text file.

## Features
- ✅ Detects exact duplicate lines (case‑sensitive).
- ✅ Reports each duplicate with the line numbers where it occurs.
- ✅ Handles missing files, empty inputs, and Unicode text gracefully.
- ✅ Designed to be **idempotent** – running it repeatedly on the same file produces identical output.

## Usage
```bash
python3 dup_check.py <path-to-your-file>
```

If duplicates are found, the script prints them in a readable format; otherwise it reports that the file is clean.

## Example
```text
$ cat sample.txt
apple
banana
apple
cherry
banana
apple

$ python3 dup_check.py sample.txt
Duplicate line "apple" found on lines: 1, 3, 6
Duplicate line "banana" found on lines: 2, 5
```

## Why this tiny project?
- Demonstrates proactive error handling (file not found, empty file, permission errors).
- Uses clear, self‑documenting variable names.
- Easy to extend (e.g., ignore whitespace, case‑insensitive mode).

---
*Created by TopherBot (topherbot@proton.me)*