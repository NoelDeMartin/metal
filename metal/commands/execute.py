import os
import click

from ..cli import cli, pass_runtime

@cli.command(name="exec")
@click.argument('command', nargs=-1)
@click.option('--service', help='Service name')
@pass_runtime
def execute(runtime, command, service):
    """Execute a command into the given service"""

    if service is None:
        service = os.path.basename(os.getcwd())

    runtime.execute_command(service, ' '.join(command))
