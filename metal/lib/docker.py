import os
import sys

from compose.config import config
from compose.project import Project as DockerComposeProject
from compose.cli.docker_client import docker_client
from compose.config.environment import Environment
from compose.config.types import VolumeSpec

from dockerpty.pty import PseudoTerminal, ExecOperation

"""
Wrapper for docker and docker-compose.

Some of the functionality in this file is fixing existing bugs or workarounds, but since the original project
(https://github.com/d11wtq/dockerpty) has not been updated for 2 years, and opened issues are ignored,
those issues haven't been reported.
"""
class Docker(object):

    def __init__(self, home_path, compose_file):
        self.home_path = home_path
        self.compose_file = compose_file

    def up(self, service_names):
        compose_project = self.__get_compose_project()
        compose_project.up(service_names, detached=True)

    def stop(self, service_names):
        compose_project = self.__get_compose_project()
        compose_project.stop(service_names)

    def down(self):
        compose_project = self.__get_compose_project()
        compose_project.down(False, True)

    def restart(self, service_names):
        compose_project = self.__get_compose_project()
        compose_project.restart(service_names)

    def open_shell(self, service_name):
        compose_project = self.__get_compose_project()
        service = compose_project.get_service(service_name)
        exec_id = service.get_container().create_exec('sh -l', stdin=True, tty=True)
        operation = ExecOperation(compose_project.client, exec_id, interactive=True)
        pty = PseudoTerminal(compose_project.client, operation)
        pty.start()

    def execute_command(self, service_name, command, volumes=[], one_off=False):
        if one_off:
            compose_project = self.__get_compose_project()
            service = compose_project.get_service(service_name)
            compose_project.initialize()
            container = service.create_container(
                one_off=True,
                command=command,
                volumes=[VolumeSpec.parse(volume) for volume in volumes]
            )
            container.start()

            for log in container.attach(stream=True, logs=True):
                sys.stdout.write(log)
                sys.stdout.flush()

            compose_project.client.remove_container(container.id, force=True, v=True)
        else:
            os.system('docker-compose --file="%s" exec -T %s %s' % (self.compose_file, service_name, command))

    def get_containers(self, service_names):
        compose_project = self.__get_compose_project()
        return compose_project.containers(service_names)

    def __get_compose_project(self):
        client = docker_client(Environment())
        config_data = config.load(
            config.ConfigDetails(
                self.home_path,
                [
                    config.ConfigFile.from_filename(self.compose_file)
                ]
            )
        )

        return DockerComposeProject.from_config(
            name='metal',
            client=client,
            config_data=config_data
        )
