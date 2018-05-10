import os
import unittest

from utils import Stubs, Cli

from mock import patch

from metal.lib.runtime import Runtime

class TestBuild(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_default_project(self, RuntimeMock):
        dir_name = os.path.basename(os.getcwd())
        RuntimeMock.return_value.installed_projects = []
        RuntimeMock.return_value.get_project.return_value = None

        result = Cli.run('build')

        RuntimeMock.return_value.get_project.assert_called_once_with(dir_name)

        assert result.exit_code != 0
        assert isinstance(result.exception, ValueError)
        assert result.exception.message == 'Project [%s] is not installed' % dir_name

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_uninstalled_project(self, RuntimeMock):
        project = Stubs.project()
        RuntimeMock.return_value.installed_projects = []
        RuntimeMock.return_value.get_project.return_value = None

        result = Cli.run('build', '--project=' + project.name)

        RuntimeMock.return_value.get_project.assert_called_once_with(project.name)

        assert result.exit_code != 0
        assert isinstance(result.exception, ValueError)
        assert result.exception.message == 'Project [%s] is not installed' % project.name

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_installed_project(self, RuntimeMock):
        project = Stubs.project()
        RuntimeMock.return_value.installed_projects = [project]
        RuntimeMock.return_value.get_project.return_value = project

        result = Cli.run('build', '--project=' + project.name)

        RuntimeMock.return_value.build_project.assert_called_once_with(project)

        assert result.exit_code == 0
        assert result.output == 'Building [%s]...\n' % project.name
