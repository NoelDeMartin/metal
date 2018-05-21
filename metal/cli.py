import click

from .lib.runtime import Runtime

pass_runtime = click.make_pass_decorator(Runtime)

@click.group()
@click.pass_context
def cli(context):
    """Forget about your bare-metal and get started right away."""
    context.obj = Runtime()

from .commands.up import up
from .commands.down import down
from .commands.ls import ls
from .commands.install import install
from .commands.uninstall import uninstall
from .commands.build import build
from .commands.shell import shell
from .commands.execute import execute
from .commands.restart import restart

if __name__ == '__main__':
   cli(click.core.Context(None))
