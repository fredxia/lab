import pdb
import click

# group command

@click.group()
@click.option("-n", help="help n")
def top_level(**kwargs):
    pass

@top_level.command(help="command1")
@click.argument("<NAME>")
def cmd1(**kwargs):
    pass

@top_level.command(help="command2")
@click.option("-n", help="help n")
@click.argument("<ARG>")
def cmd2(**kwargs):
    pass

top_level()
