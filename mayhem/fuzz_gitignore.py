#!/usr/bin/env python3
"""Atheris fuzz harness for gitignore_parser.

Ported from the fork's original Mayhem target (Bailey Capuano). Atheris
instruments the imported gitignore_parser module (coverage), so libFuzzer drives
the parser toward new code paths. The harness writes the fuzzed bytes to a
temporary .gitignore file, parses it via parse_gitignore(), then probes the
returned matcher with fuzzer-generated paths.

Run modes (driven by the compiled launcher `gitignore_fuzzer` / `-standalone`):
  * fuzzing      — `python3 fuzz_gitignore.py [libFuzzer args]`
  * single input — `python3 fuzz_gitignore.py <file>` (libFuzzer runs it once)
"""

import atheris
import sys
import fuzz_helpers
import random

with atheris.instrument_imports(include=["gitignore_parser"]):
    from gitignore_parser import parse_gitignore


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    try:
        with fdp.ConsumeTemporaryFile(".gitignore", all_data=False, as_bytes=False) as name:
            matches = parse_gitignore(name)
            for _ in range(fdp.ConsumeIntInRange(0, 20)):
                matches('/tmp/' + fdp.ConsumeRandomString())
    except (ValueError, IndexError) as e:
        if random.random() > 0.999:
            raise e
        return -1


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
