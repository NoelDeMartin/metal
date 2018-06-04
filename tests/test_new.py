import os
import unittest

from utils import Stubs, Cli

from mock import patch

from metal.lib.project import Project
from metal.lib.runtime import Runtime

class TestNew(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_new_project(self, RuntimeMock):
        path = os.getcwd()
        project_name = 'foobar'
        RuntimeMock.return_value.get_project.return_value = None

        result = Cli.run('new', project_name, '--framework=laravel')

        RuntimeMock.return_value.get_project.assert_called_once_with(project_name)
        RuntimeMock.return_value.create_project.assert_called_once_with(project_name, path, 'laravel')

        assert result.exit_code == 0
        assert result.output == 'Creating [%s]...\n' % project_name
