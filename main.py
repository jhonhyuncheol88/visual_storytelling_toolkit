from __future__ import annotations

import os
import sys


def _ensure_src_on_path() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(here, "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)


def main() -> None:
    _ensure_src_on_path()
    from cinescribe.app import main as app_main

    app_main()


if __name__ == "__main__":
    main()


