# Portable paths

**Claim:** every path in a repository can be checked out on any common filesystem.

- **Grade:** convention (a platform specification).
- **Evidence:** [against](../../evidence/file-structure/against.md) (portable paths).
- **Check:** `portable-paths` (exact).
- **Reader styles:** none override it.

## What it asks

- No `: * ? " < > | \` and no control characters in a path component.
- No leading or trailing space, no space before the extension, no trailing period.
- No reserved device name (CON, PRN, AUX, NUL, COM1 to COM9, LPT1 to LPT9), even with an extension.
- No two paths differing only by case; no versioned symbolic link.
- Paths shorter than 260 characters.

## Why

A path one filesystem cannot create aborts the checkout and leaves the clone half-written. Windows reserves these
characters and names and caps path length unless long paths are enabled (Microsoft 2024).

## Limits

Accented names may be stored decomposed on macOS and recomposed by git only when configured to (Git 2023).
