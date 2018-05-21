import os
import click

from ..cli import cli, pass_runtime
from ..lib.project import Project

@cli.command()
@click.option('--name', help='Project name')
@click.option('--path', help='Project path')
@click.option('--framework', type=click.Choice(['laravel', 'rails']), help='Project framework')
@pass_runtime
def install(runtime, name, path, framework):
    """Install new project"""

    if path is None:
        path = os.getcwd()

    if name is None:
        name = os.path.basename(path)

    if framework is None:
        if os.path.isfile(path + '/bin/rails'):
            framework = 'rails'
        elif os.path.isfile(path + '/artisan'):
            framework = 'laravel'
        else:
            framework = 'laravel'

    project = runtime.get_project(name)
    if project is None:
        project = Project(name, path, framework)
    elif project.path != path:
        raise ValueError('Project [%s] is already installed from a different path (%s)' % (name, path))

    if not project.installed:
        click.echo('Installing [%s]...' % project.name)
        runtime.install_project(project)
        runtime.build_project(project)
