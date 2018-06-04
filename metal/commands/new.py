import os
import click

from ..cli import cli, pass_runtime

@cli.command()
@click.argument('name')
@click.option('--path', help='Project path')
@click.option('--framework', type=click.Choice(['laravel', 'rails']), default='laravel', help='Project framework')
@pass_runtime
def new(runtime, name, path, framework):
    """Create new project"""

    if path is None:
        path = os.getcwd()

    project = runtime.get_project(name)
    if project is None:
        click.echo('Creating [%s]...' % name)
        runtime.create_project(name, path, framework)
    else:
        raise ValueError('Project [%s] already exists, use a different name' % name)
