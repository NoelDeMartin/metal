import os
import re

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
    def project(cls, installed=False, active=False, framework='laravel', path=None, name=None):
        if path is None:
            path = os.path.dirname(cls.fake.file_path())
        if name is None:
            name = re.sub(r'\W+', '-', cls.fake.company()).lower()
        project = Project(name, path, framework)
        project.installed = installed
        project.active = active

        return project
