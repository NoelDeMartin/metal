import os
import unittest

from utils import Stubs, Cli

from mock import patch

from metal.lib.project import Project
from metal.lib.runtime import Runtime

class TestUp(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_default(self, RuntimeMock):
        projects = [
            Stubs.project(True),
            Stubs.project(True),
        ]
        RuntimeMock.return_value.installed_projects = projects

        with patch.object(
            RuntimeMock.return_value,
            'activate_project',
            wraps=self.stub_activate_project
        ) as activate_project_mock:

            result = Cli.run('up')

            assert activate_project_mock.call_count == 2
            assert activate_project_mock.call_args_list[0][0][0] == projects[0]
            assert activate_project_mock.call_args_list[1][0][0] == projects[1]

            assert result.exit_code == 0
            assert result.output == \
                'Starting [%s]...\n' % projects[0].name + \
                'Starting [%s]...\n' % projects[1].name + \
                '[%s] running @ %s\n' % (projects[0].name, 'http://%s.test' % projects[0].name) + \
                '[%s] running @ %s\n' % (projects[1].name, 'http://%s.test' % projects[1].name)

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_only_flag(self, RuntimeMock):
        dir_name = os.path.basename(os.getcwd())
        project = Stubs.project(True, name=dir_name)
        RuntimeMock.return_value.installed_projects = [
            project,
            Stubs.project(True),
        ]

        with patch.object(
            RuntimeMock.return_value,
            'activate_project',
            wraps=self.stub_activate_project
        ) as activate_project_mock:

            result = Cli.run('up', '--only')

            activate_project_mock.assert_called_once_with(project)

            assert result.exit_code == 0
            assert result.output == \
                'Starting [%s]...\n' % project.name + \
                '[%s] running @ %s\n' % (project.name, 'http://%s.test' % project.name)

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_projects_option(self, RuntimeMock):
        projects = [
            Stubs.project(True),
            Stubs.project(True),
        ]
        RuntimeMock.return_value.installed_projects = [
            projects[0],
            projects[1],
            Stubs.project(True),
        ]

        with patch.object(
            RuntimeMock.return_value,
            'activate_project',
            wraps=self.stub_activate_project
        ) as activate_project_mock:

            result = Cli.run('up', '--projects=' + ','.join([projects[0].name, projects[1].name]))

            assert activate_project_mock.call_count == 2
            assert activate_project_mock.call_args_list[0][0][0] == projects[0]
            assert activate_project_mock.call_args_list[1][0][0] == projects[1]

            assert result.exit_code == 0
            assert result.output == \
                'Starting [%s]...\n' % projects[0].name + \
                'Starting [%s]...\n' % projects[1].name + \
                '[%s] running @ %s\n' % (projects[0].name, 'http://%s.test' % projects[0].name) + \
                '[%s] running @ %s\n' % (projects[1].name, 'http://%s.test' % projects[1].name)

    def stub_activate_project(self, project):
        project.active = True
