import click

from ..cli import cli, pass_runtime

@cli.command()
@click.option('--only', help='Comma separated list of projects to restart')
@pass_runtime
def restart(runtime, only):
    """Restart projects"""

    if only is None:
        only = map(lambda project: project.name, runtime.active_projects)
    else:
        only = only.split(',')

    for project in runtime.active_projects:
        if project.name in only:
            click.echo('Restarting [%s]...' % project.name)
            runtime.restart_project(project)

    runtime.sync_services()
