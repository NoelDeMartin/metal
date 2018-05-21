import click

from ..cli import cli, pass_runtime

@cli.command()
@click.option('--only', help='Comma separated list of projects to start')
@pass_runtime
def up(runtime, only):
    """Start projects"""

    if only is None:
        only = map(lambda project: project.name, runtime.installed_projects)
    else:
        only = only.split(',')

    for project in runtime.installed_projects:
        if not project.active and project.name in only:
            click.echo('Starting [%s]...' % project.name)
            runtime.activate_project(project)

    runtime.sync_services()

    for project in runtime.installed_projects:
        if project.active:
            click.echo('[%s] running @ %s' % (project.name, 'http://%s.test' % project.name))
