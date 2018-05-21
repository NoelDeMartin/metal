import os
import click

from ..cli import cli, pass_runtime
from ..lib.project import Project

@cli.command()
@click.option('--project', help='Project name')
@pass_runtime
def uninstall(runtime, project):
    """Uninstall project"""

    if project is None:
        project_name = os.path.basename(os.getcwd())
    else:
        project_name = project

    project = runtime.get_project(project_name)
    if project is None:
        raise ValueError('Project [%s] is not installed' % project_name)
    else:
        click.echo('Uninstalling [%s]...' % project.name)
        if project.active:
            runtime.deactivate_project(project)
        runtime.uninstall_project(project)
