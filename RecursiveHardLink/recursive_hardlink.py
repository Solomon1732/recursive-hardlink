#!/usr/bin/env python3
"""
Run the main function.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path


def resolve_parents(directory: Path) -> Path:
    """Resolve the parent directories of 'directory'."""

    resolved_dir: Path = directory.resolve()
    parent: Path = resolved_dir.parent.resolve(strict=True)
    dir_name = resolved_dir.name

    return Path(parent, dir_name)


def main() -> None:
    """Main function of the module."""

    parser = argparse.ArgumentParser(
        description=(
            "Recursively hard link the directory 'source' and its content to 'dest'."
            " If 'source' or the parent directories of 'dest' don't exist then the"
            " program exits with an error. By default symbolic links are not followed."
        ),
    )
    parser.add_argument(
        "-s",
        "--follow-symlinks",
        action="store_true",
        help="always follow symbolic links",
    )
    parser.add_argument("source", type=Path, help="source directory to be traversed")
    parser.add_argument(
        "dest", type=Path, help="the name of the directory to be created"
    )
    args = parser.parse_args()
    follow_symlinks: bool = args.follow_symlinks
    source: Path = args.source.resolve(strict=True)
    dest: Path = resolve_parents(directory=args.dest)

    shutil.copytree(
        src=source, dst=dest, symlinks=follow_symlinks, copy_function=os.link
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted by user. Exiting...")
    except FileExistsError as e:
        sys.exit(f"Error: {e}.")
