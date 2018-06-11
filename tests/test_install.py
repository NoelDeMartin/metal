import os
import unittest

from utils import Stubs, Cli

from mock import patch

from metal.lib.project import Project
from metal.lib.runtime import Runtime

class TestInstall(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_new_project(self, RuntimeMock):
        dir_name = os.path.basename(os.getcwd())
        RuntimeMock.return_value.get_project.return_value = None

        result = Cli.run('install', '--framework=laravel')

        RuntimeMock.return_value.get_project.assert_called_once_with(dir_name)
        RuntimeMock.return_value.install_project.assert_called_once()
        RuntimeMock.return_value.build_project.assert_called_once()

        project = RuntimeMock.return_value.install_project.call_args[0][0]
        isinstance(project, Project)
        assert project.name == dir_name
        assert project.framework == 'laravel'

        project = RuntimeMock.return_value.build_project.call_args[0][0]
        isinstance(project, Project)
        assert project.name == dir_name
        assert project.framework == 'laravel'

        assert result.exit_code == 0
        assert result.output == 'Installing [%s]...\n' % dir_name

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_project_name_slugify(self, RuntimeMock):
        RuntimeMock.return_value.get_project.return_value = None
        name = 'Foobar and sons'
        slug = 'foobar-and-sons'
        result = Cli.run('install', '--name=' + name, '--framework=rails')

        RuntimeMock.return_value.get_project.assert_called_once_with('foobar-and-sons')
        RuntimeMock.return_value.install_project.assert_called_once()
        RuntimeMock.return_value.build_project.assert_called_once()

        project = RuntimeMock.return_value.install_project.call_args[0][0]
        isinstance(project, Project)
        assert project.name == slug
        assert project.framework == 'rails'

        project = RuntimeMock.return_value.build_project.call_args[0][0]
        isinstance(project, Project)
        assert project.name == slug
        assert project.framework == 'rails'

        assert result.exit_code == 0
        assert result.output == 'Installing [%s]...\n' % slug
