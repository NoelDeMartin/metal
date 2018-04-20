import os
import click

from ..cli import cli, pass_runtime
from ..lib.project import Project

@cli.command()
@click.option('--name', help='Project name')
@click.option('--path', help='Project path')
@pass_runtime
def install(runtime, name, path):
    """Install new project"""

    if path is None:
        path = os.getcwd()

    if name is None:
        name = os.path.basename(path)

    project = runtime.get_project(name)
    if project is None:
        project = Project(name, path)
    elif project.path != path:
        raise ValueError('Project [%s] is already installed from a different path (%s)' % (name, path))

    if not project.installed:
        click.echo('Installing [%s]...' % project.name)
        runtime.install_project(project)
        runtime.build_project(project)
