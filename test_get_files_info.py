import textwrap

from functions.get_files_info import get_files_info


def show(label: str, directory: str) -> None:
    result = get_files_info("calculator", directory)
    indent = "    " if result.startswith("Error:") else "  "
    print(f"Result for {label}:")
    print(textwrap.indent(result, indent))
    print()


def main():
    show("current directory", ".")
    show("'pkg' directory", "pkg")
    show("'/bin' directory", "/bin")
    show("'../' directory", "../")


if __name__ == "__main__":
    main()
