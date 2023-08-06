"""
Return a text code for every input.
"""
import select
import sys
import tty


def test_stdin(timeout=0.5):
    fno = sys.stdin.fileno()
    tty.setraw(fno)

    res = sys.stdin.read(1)  # Blocking
    rfds, _, _ = select.select([fno], [], [], timeout)

    while sys.stdin.fileno() in rfds or sys.stdin in rfds:
        res += sys.stdin.read(1)
        rfds, _, _ = select.select([sys.stdin.fileno()], [], [], 0)

    return res


def main():
    print("Starting stdin tests")
    while True:
        v = test_stdin()
        print(f"{v=!r}")
        if v == "q":
            break


if __name__ == "__main__":
    main()
