#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports(include=["gitignore_parser"]):
    from gitignore_parser import parse_gitignore


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with fdp.ConsumeTemporaryFile(".gitignore", all_data=False, as_bytes=False) as name:
            matches = parse_gitignore(name)
            for _ in range(fdp.ConsumeIntInRange(0, 100)):
                matches('/tmp/' + fdp.ConsumeRandomString())
    except ValueError:
        return -1

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
