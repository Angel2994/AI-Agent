from functions.run_python_file import run_python_file


def show(file_path: str, args: list[str] | None = None) -> None:
    label = f"{file_path} {args}" if args else file_path
    print(f"Result for {label}:")
    print(run_python_file("calculator", file_path, args))
    print()


def main():
    show("main.py")
    show("main.py", ["3 + 5"])
    show("tests.py")
    show("../main.py")
    show("nonexistent.py")
    show("lorem.txt")


if __name__ == "__main__":
    main()
