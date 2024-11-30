import click
import package
import package.main


@click.group
def cli() -> None:
    pass


@cli.command
@click.argument("target")
def say_hello(target: str) -> None:
    print(f"Hello {target}")


@cli.command
def use_submodule() -> None:
    print(f"Hello {__name__}: {__file__}")
    package.main.main()


@cli.command
@click.option("--first", "-a", required=True, type=int)
@click.option("--second", "-b", default=0)
def add(first: int, second: int) -> None:
    print(f"{first} + {second} = {first + second}")


if __name__ == "__main__":
    cli()
