import os
import unittest

from utils import Stubs, Cli

from mock import patch

from metal.lib.project import Project
from metal.lib.runtime import Runtime

class TestUninstall(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_existing_project(self, RuntimeMock):
        project = Stubs.project(True)
        RuntimeMock.return_value.get_project.return_value = project

        result = Cli.run('uninstall', '--project=' + project.name)

        RuntimeMock.return_value.uninstall_project.assert_called_once_with(project)

        assert result.exit_code == 0
        assert result.output == 'Uninstalling [%s]...\n' % project.name

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_active_project(self, RuntimeMock):
        project = Stubs.project(True, True)
        RuntimeMock.return_value.get_project.return_value = project

        result = Cli.run('uninstall', '--project=' + project.name)

        RuntimeMock.return_value.deactivate_project.assert_called_once_with(project)
        RuntimeMock.return_value.uninstall_project.assert_called_once_with(project)

        assert result.exit_code == 0
        assert result.output == 'Uninstalling [%s]...\n' % project.name
