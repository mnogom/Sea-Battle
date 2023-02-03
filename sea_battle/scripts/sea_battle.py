#!/usr/bin/env python3

"""Entrypoint."""

import sys

from sea_battle.engine import play


def main() -> None:
    """Main function."""

    try:
        play()
    except KeyboardInterrupt:
        print("\nGood luck!")
        sys.exit(0)


if __name__ == '__main__':
    main()
