import os
import click

from ..cli import cli, pass_runtime

@cli.command()
@click.option('--projects', help='Comma separated list of projects to start')
@click.option('--only', help='Start only current project', is_flag=True)
@pass_runtime
def up(runtime, projects, only):
    """Start projects"""

    if only:
        projects = [os.path.basename(os.getcwd())]
    elif projects is None:
        projects = map(lambda project: project.name, runtime.installed_projects)
    else:
        projects = projects.split(',')

    for project in runtime.installed_projects:
        if not project.active and project.name in projects:
            click.echo('Starting [%s]...' % project.name)
            runtime.activate_project(project)

    runtime.sync_services()

    for project in runtime.installed_projects:
        if project.active:
            click.echo('[%s] running @ %s' % (project.name, 'http://%s.test' % project.name))
