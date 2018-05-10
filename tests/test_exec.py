import os
import unittest

from utils import Cli

from mock import patch

from metal.lib.runtime import Runtime

class TestExec(unittest.TestCase):

    @patch('metal.cli.Runtime', spec=Runtime)
    def test_exec(self, RuntimeMock):
        dir_name = os.path.basename(os.getcwd())
        command = 'foo bar'

        result = Cli.run('exec', command)

        assert result.exit_code == 0
        RuntimeMock.return_value.execute_command.assert_called_with(dir_name, command)
