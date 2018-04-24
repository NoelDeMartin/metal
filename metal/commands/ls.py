import click

from ..cli import cli, pass_runtime

@cli.command()
@pass_runtime
def ls(runtime):
    """List projects with status"""

    if len(runtime.installed_projects) == 0:
        click.echo('There are no projects installed, run metal install to install new projects')
    else:
        for project in runtime.installed_projects:
            if project.active:
                click.echo('[%s] running @ %s' % (project.name, 'http://%s.test' % project.name))
            else:
                click.echo('[%s] stopped' % project.name)
