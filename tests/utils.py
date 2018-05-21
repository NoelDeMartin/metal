import os

from faker import Faker

from click.testing import CliRunner

from metal.lib.project import Project
from metal.cli import cli

class Cli():

    runner = CliRunner()

    @classmethod
    def run(cls, *args):
        return cls.runner.invoke(cli, args)

class Stubs():

    fake = Faker()

    @classmethod
    def project(cls, installed=False, active=False, framework='laravel'):
        project = Project(cls.fake.company(), os.path.dirname(cls.fake.file_path()), framework)
        project.installed = installed
        project.active = active

        return project
