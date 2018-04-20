import os
import click

from ..cli import cli, pass_runtime

@cli.command()
@click.option('--service', help='Service name')
@pass_runtime
def shell(runtime, service):
    """Open a shell into the given service"""

    if service is None:
        service = os.path.basename(os.getcwd())

    runtime.open_shell(service)
