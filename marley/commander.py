import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def main():
    console.print(
        Panel.fit(
            "[bold green]MARLEY OS[/bold green]\n"
            "One Commander. Multiple Missions. Infinite Context.\n\n"
            "[green]Status:[/green] ONLINE\n"
            "[magenta]Mission:[/magenta] Genesis",
            title="COMMANDER",
            border_style="magenta"
        )
    )

if __name__ == "__main__":
    app()
