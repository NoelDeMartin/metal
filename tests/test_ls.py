import unittest

from utils import Stubs, Cli

from mock import patch

from metal.lib.runtime import Runtime

class TestLs(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_without_projects(self, RuntimeMock):
        RuntimeMock.return_value.installed_projects = []

        result = Cli.run('ls')

        assert result.exit_code == 0
        assert result.output == 'There are no projects installed, run metal install to install new projects\n'

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_stopped_projects(self, RuntimeMock):
        project = Stubs.project()
        RuntimeMock.return_value.installed_projects = [project]

        result = Cli.run('ls')

        assert result.exit_code == 0
        assert result.output == '[%s] stopped\n' % project.name

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_ongoing_projects(self, RuntimeMock):
        project = Stubs.project(True, True)
        RuntimeMock.return_value.installed_projects = [project]

        result = Cli.run('ls')

        assert result.exit_code == 0
        assert result.output == '[%s] running @ http://%s.test\n' % (project.name, project.name)

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_mixed_projects(self, RuntimeMock):
        projects = [
            Stubs.project(True, True),
            Stubs.project(),
        ]
        RuntimeMock.return_value.installed_projects = projects

        result = Cli.run('ls')

        assert result.exit_code == 0
        assert result.output == '[%s] running @ http://%s.test\n[%s] stopped\n' % (projects[0].name, projects[0].name, projects[1].name)
