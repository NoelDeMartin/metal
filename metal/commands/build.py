import os
import click

from ..cli import cli, pass_runtime

@cli.command()
@click.option('--project', help='Project name')
@pass_runtime
def build(runtime, project):
    """Build project dependencies"""

    if project is None:
        project_name = os.path.basename(os.getcwd())
    else:
        project_name = project

    project = runtime.get_project(project_name)
    if project is None:
        raise ValueError('Project [%s] is not installed' % project_name)
    else:
        click.echo('Building [%s]...' % project.name)
        runtime.build_project(project)
