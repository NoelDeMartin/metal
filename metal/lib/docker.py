import os
import sys

from compose.config import config
from compose.project import Project as DockerComposeProject
from compose.cli.docker_client import docker_client
from compose.config.environment import Environment
from compose.config.types import VolumeSpec

from dockerpty.pty import ExecOperation, io, tty

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

    def execute_command(self, service_name, command, volumes=[], one_off=False):
        compose_project = self.__get_compose_project()
        service = compose_project.get_service(service_name)

        if one_off:
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
            exec_id = service.get_container().create_exec(command, stdin=True, tty=True)
            self.__start_operation(ExecOperation(compose_project.client, exec_id, interactive=True))

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

    ## Copied from https://github.com/d11wtq/dockerpty/blob/master/dockerpty/pty.py#L327
    def __start_operation(self, operation):
        pumps = operation.start()
        pumps[0].propagate_close = False

        flags = [p.set_blocking(False) for p in pumps]

        try:
            self.__hijack_tty(operation, pumps)
        finally:
            if flags:
                for (pump, flag) in zip(pumps, flags):
                    if not pump.fileno() == -1:
                        io.set_blocking(pump, flag)

    def __hijack_tty(self, operation, pumps):
        with tty.Terminal(operation.stdin, raw=operation.israw()):
            stdin_fileno = sys.stdin.fileno()
            stdout_fileno = sys.stdout.fileno()
            pipe_silenced = False
            while True:
                read_pumps = [p for p in pumps if not self.__pump_closed(p)]
                write_streams = [p.to_stream for p in pumps if not self.__pump_closed(p) and p.to_stream.needs_write()]

                read_ready, write_ready = io.select(read_pumps, write_streams, timeout=60)

                for write_stream in write_ready:
                    write_stream.do_write()

                for pump in read_ready:
                    # TODO may have issues with input files longer than this
                    read = pump.from_stream.read(4096)

                    if read is None or len(read) == 0:
                        pump.eof = True
                        if pump.propagate_close:
                            pump.to_stream.close()
                        continue

                    if pump.to_stream.fileno() == stdout_fileno and not pipe_silenced and not os.isatty(stdin_fileno):
                        pipe_silenced = True
                    else:
                        pump.to_stream.write(read)

                if all([p.is_done() or self.__pump_closed(p) for p in pumps]):
                    break

    def __pump_closed(self, pump):
        return pump.eof or pump.from_stream.fileno() == -1 or pump.to_stream.fileno() == -1
