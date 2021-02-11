import typer

app = typer.Typer()


@app.command()
def run():
    typer.echo("Hello World!")
