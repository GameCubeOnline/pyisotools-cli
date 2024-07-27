import sys

from pathlib import Path
from typing import Optional, Tuple

from pyisotools import __version__
from pyisotools.iso import GamecubeISO


def main(argv: Optional[Tuple] = None):
    if argv is None:
        argv = sys.argv[1:]

    # Force Windows Taskbar Icon
    if sys.platform in {"win32", "cygwin", "msys"}:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            Controller.get_window_title()
        )

        from argparse import ArgumentParser

        parser = ArgumentParser(
            f"pyisotools v{__version__}", description="ISO tool for extracting/building Gamecube ISOs", allow_abbrev=False)

        parser.add_argument("src", help="ISO/root to build/extract with")
        parser.add_argument("job",
                            choices=["B", "E"],
                            help="Job to do")
        parser.add_argument("--newinfo",
                            help="Overwrite original information with custom info (build only)",
                            action="store_true")
        parser.add_argument("--dest",
                            help="Directory (extract)/ISO (build) to store data")

        args = parser.parse_args(args=argv)

        src = Path(args.src).resolve()
        if args.job == "E":
            iso = GamecubeISO.from_iso(src)
            iso.extract(args.dest)
        elif args.job == "B":
            iso = GamecubeISO.from_root(src, genNewInfo=args.newinfo)
            iso.build(args.dest)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
