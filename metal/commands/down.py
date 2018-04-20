import click

from ..cli import cli, pass_runtime

@cli.command()
@click.option('--only', help='Comma separated list of projects to start')
@pass_runtime
def down(runtime, only):
    """Stop projects"""

    if only is None:
        only = map(lambda project: project.name, runtime.active_projects)
    else:
        only = only.split(',')

    for project in tuple(runtime.active_projects):
        if project.name in only:
            click.echo('Stopping [%s]...' % project.name)
            runtime.deactivate_project(project)

    runtime.sync_services()
