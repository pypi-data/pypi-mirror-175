import typer
import subprocess
import os
import shutil

app = typer.Typer()

@app.command()
def init():
    typer.echo("Projekt wird initialisiert")
    github = "https://github.com/Coding-Crashkurse/npm-demo-repo"

    projektpath = os.path.join("C:\\", "Users", "User", ".cookiecutters", github.split("/")[-1])
    if os.path.exists(projektpath):
        shutil.rmtree(projektpath)

    subprocess.run(["cookiecutter", "https://github.com/Coding-Crashkurse/npm-demo-repo"])


@app.command()
def delete():
    directories = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    if len(directories) > 1:
        delyn = typer.confirm(f"WARNUNG: Es wurden mehrere Folder gefunden: {','.join(directories)} - Alle löschen?")
        if delyn:
            for _dir in directories:
                shutil.rmtree(_dir)
    elif len(directories) == 1:
        delyn = typer.confirm(f"Folder {directories[0]} löschen? [Y/N")
        if delyn:
            shutil.rmtree(directories[0])
    else:
        typer.echo("WARNUNG: Es wurden keine folder gefunden")

