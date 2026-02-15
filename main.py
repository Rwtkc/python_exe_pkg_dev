import datetime
import platform
import sys


def main() -> None:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("GitHub Actions EXE build test")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    print(f"Time: {now}")


if __name__ == "__main__":
    main()
