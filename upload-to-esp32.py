#!/usr/bin/env python3
"""
mp-helper – cross-platform helper around `mpremote`

Sub-commands
------------
mp-helper list
    Print all detected MicroPython-compatible serial devices.

mp-helper upload
    Upload the files defined in FILE_PATTERNS (wildcards allowed)
    to a chosen device (interactive dropdown).

mp-helper dev
    Run the `main.py` that is in the current directory on a
    chosen device (interactive dropdown).

Device shortcuts
----------------
a<n> → /dev/ttyACMn (Linux/macOS) u<n> → /dev/ttyUSBn (Linux/macOS)
c<n> → COM<n> (Windows)
"""

import argparse, glob, os, platform, re, subprocess, sys, textwrap
from pathlib import Path
from typing import List, Optional, Tuple

# ------------------------------  USER SETTINGS  ------------------------------

# Edit this list (wildcards allowed) – all matching files are uploaded by
# `mp-helper upload`.  Relative paths are resolved from the script’s cwd.
FILE_PATTERNS: List[str] = [
    "boot.py",
    "main.py",
    "menu.py",
    "pin_values.py",
    "happy_meter.py",
    "buzzer_sounds.py",
    "MPU6050.py",
    "oled_functions.py",
    "lib/**/*.py",
    "*.bmp",
]

# -----------------------------------------------------------------------------


# === Serial-port discovery (cross-platform) ==================================
def _iter_pyserial_ports() -> List[Tuple[str, str]]:
    """
    Return list of (device, description) tuples, using pyserial if available,
    else minimal fall-back scanning.  Works on Linux, macOS, Windows.
    """
    try:
        import serial.tools.list_ports  # pyserial ≥3.0
        return [(p.device, p.description) for p in serial.tools.list_ports.comports()]
    except ImportError:                      # noqa: E722  (fallback)
        pat = {
            "Linux":  ["/dev/ttyACM*", "/dev/ttyUSB*"],
            "Darwin": ["/dev/tty.*", "/dev/cu.*"],
            "Windows": [r"COM[0-9]*"],
        }[platform.system()]
        devices: List[str] = []
        for g in pat:
            devices.extend(glob.glob(g))
        return [(d, "Serial port") for d in sorted(set(devices))]


def _resolve_shortcut(arg: str) -> str:
    """
    Map a/u/c shortcuts to real paths, otherwise return arg unchanged.
    """
    if re.fullmatch(r"[auc]\d+", arg):
        prefix, n = arg[0], int(arg[1:])
        osname = platform.system()
        if osname == "Windows":          # c<num> = COM<num>
            return f"COM{n}" if prefix == "c" else arg
        # *nix
        if prefix == "a":
            return f"/dev/ttyACM{n}"
        if prefix == "u":
            return f"/dev/ttyUSB{n}"
    return arg


# === Helpers =================================================================
def _pick_device() -> str:
    """
    Print an interactive numeric dropdown of detected devices and return the
    chosen port/path.
    """
    devices = _iter_pyserial_ports()
    if not devices:
        sys.exit("No serial devices found.")
    print("Select device:")
    for i, (dev, desc) in enumerate(devices):
        print(f"  [{i}] {dev:15} {desc}")
    while True:
        try:
            choice = int(input("Enter number: "))
            return devices[choice][0]
        except (ValueError, IndexError):
            print("Invalid selection, try again.")


def _run_mpremote(*mpremote_args: str) -> None:
    """
    Execute mpremote with the supplied arguments.
    """
    cmd = ["mpremote", *mpremote_args]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        sys.exit("mpremote not found. `pip install mpremote` first.")
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


# === Sub-commands ============================================================
def cmd_list(_: argparse.Namespace) -> None:
    """
    mp-helper list
    """
    for dev, desc in _iter_pyserial_ports():
        print(f"{dev:15} {desc}")


def cmd_upload(_: argparse.Namespace) -> None:
    """
    mp-helper upload
    """
    port = _pick_device()
    files: List[Path] = []
    for pattern in FILE_PATTERNS:
        files.extend(Path().glob(pattern))
    if not files:
        sys.exit("No files matched FILE_PATTERNS.")
    for f in files:
        print(f"Uploading {f} → {port} …")
        _run_mpremote("connect", port, "fs", "cp", str(f), ":")
    print("Done.")


def cmd_dev(_: argparse.Namespace) -> None:
    """
    mp-helper dev
    """
    port = _pick_device()
    main_local = Path("main.py")
    if not main_local.exists():
        sys.exit("main.py not found in current directory.")
    print(f"Uploading main.py → {port} and running …")
    _run_mpremote("connect", port, "fs", "cp", "main.py", ":")
    _run_mpremote("connect", port, "exec", "import main")


# === CLI entrypoint ==========================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mp-helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list",  help="List attached devices").set_defaults(func=cmd_list)
    sub.add_parser("upload", help="Upload files defined in FILE_PATTERNS").set_defaults(func=cmd_upload)
    sub.add_parser("dev",   help="Run main.py on device").set_defaults(func=cmd_dev)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
