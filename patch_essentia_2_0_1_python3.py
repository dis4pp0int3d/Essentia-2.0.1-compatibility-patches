#!/usr/bin/env python3
"""Make Essentia 2.0.1's algorithm scanner parse under Python 3."""

from pathlib import Path
import shutil
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: patch_essentia_2_0_1_python3.py <essentia-source-root>")
        return 2

    source_root = Path(sys.argv[1]).resolve()
    target = source_root / "utils" / "algorithms_info.py"
    if not target.is_file():
        print(f"Could not find Essentia build helper: {target}")
        return 2

    original = target.read_text(encoding="utf-8")
    updated = original

    replacements = [
        (
            "                    print 'WARNING: file \"%s\" does not seem to contain an algorithm.' % filename",
            "                    print('WARNING: file \"%s\" does not seem to contain an algorithm.' % filename)",
        ),
        (
            "                    print 'ERROR: file \"%s\" contains both standard and streaming'\\\n"
            "                          'version of the algorithm, but they have different '\\\n"
            "                          'names: %s != %s.' %(filename, algo, salgo)",
            "                    print('ERROR: file \"%s\" contains both standard and streaming'\n"
            "                          'version of the algorithm, but they have different '\n"
            "                          'names: %s != %s.' % (filename, algo, salgo))",
        ),
        (
            "                print 'Error while trying to parse file \"%s\"' % filename",
            "                print('Error while trying to parse file \"%s\"' % filename)",
        ),
        (
            "        print name, ':\\n',",
            "        print(name, ':\\n', end=' ')",
        ),
        (
            "            print '  %s: %s' % (attr, algo[attr])",
            "            print('  %s: %s' % (attr, algo[attr]))",
        ),
        (
            "        print\n",
            "        print()\n",
        ),
    ]

    changes = 0
    for old, new in replacements:
        if old in updated:
            updated = updated.replace(old, new, 1)
            changes += 1
        elif new not in updated:
            print("Patch stopped: the expected Essentia 2.0.1 source text was not found.")
            return 1

    if not changes:
        print("Essentia algorithm scanner is already Python 3 compatible.")
        return 0

    backup = target.with_name(target.name + ".python2-backup")
    if not backup.exists():
        shutil.copy2(target, backup)

    with target.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(updated)

    print(f"Updated {target}; original saved as {backup.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
