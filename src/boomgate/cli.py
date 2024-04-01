import typer
from rich.table import Table
from rich.console import Console
from .ecosystems.pypi import PyPI, PyPIPackage
from .logging import configure_logging
from typing import Annotated
from .inspect import inspect_package

console = Console()


cli = typer.Typer()


@cli.command()
def inspect(
    name: Annotated[
        str, typer.Argument(help="The name of the package you wish to inspect.")
    ],
    version: Annotated[str, typer.Argument(help="The package version to inspect.")],
    debug: bool = typer.Option(default=False, help="Enable debug mode."),
):
    configure_logging(level="DEBUG" if debug else "INFO", console=console)

    with console.status("Getting package info..."):
        package: PyPIPackage = PyPI.get_package(name)
    print_package_info(package)
    console.print()

    with console.status(f"Inspecting version [green]{version}[/green]..."):
        if version not in package.versions:
            console.print(f"[red]Version {version} not found in package {name}.[/red]")
            raise typer.Exit(1)
        result = inspect_package(package, package.versions[version])  # type: ignore

    if result:
        table = Table(
            title="Risks", title_style="red bold", show_header=False, show_lines=True
        )
        table.add_column("Summary", style="bold")
        table.add_column("Description")
        for risk_type, risks in result.items():
            risk_type_name = risk_type.name_plural if len(risks) > 1 else risk_type.name
            risk_type_description = (
                risk_type.description_plural
                if len(risks) > 1 and risk_type.description_plural
                else risk_type.description
            )

            list_entries = []
            try:
                for risk in risks:
                    list_entries.append(risk.description_plural_list)
            except NotImplementedError:
                list_entries = []

            if list_entries:
                risk_type_description += " [bright_black]"
                risk_type_description += ", ".join(list_entries[:3])
                if len(list_entries) > 3:
                    risk_type_description += f", and {len(list_entries) - 3} more."
                risk_type_description += "[/bright_black]"

            table.add_row(risk_type_name, risk_type_description)

        console.print(table)
    else:
        console.print(
            f"[green][bold]{package.name} {version} has no risks.[/bold][/green]"
        )


def print_package_info(package):
    table = Table(
        title=f"[bold blue]Package info:[/bold blue] {package.name}",
        show_header=False,
        show_lines=True,
    )
    table.add_column(style="bold")
    if package.description:
        table.add_row("Description", package.description)
    if package.license:
        table.add_row("License", package.license)
    if package.author_name or package.author_email:
        if package.author_name and package.author_email:
            table.add_row(
                "Author", name_email_output(package.author_name, package.author_email)
            )
    if package.maintainer_name or package.maintainer_email:
        if package.maintainer_name and package.maintainer_email:
            table.add_row(
                "Maintainer",
                name_email_output(package.maintainer_name, package.maintainer_email),
            )
    console.print(table)


def name_email_output(name, email) -> str:
    if name and email:
        return f"{name} <[underline]{email}[/underline]>"
    elif name:
        return name
    else:
        return email


def main():
    cli()
