def desc() -> str:
    return f"{__name__}: {__file__}"


def main() -> None:
    print(f"Hello {desc()}")


if __name__ == "__main__":
    main()
