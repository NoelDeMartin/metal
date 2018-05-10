import os
import re
import sys
import json
import metal

from .project import Project

from shutil import copyfile

from compose.config import config
from compose.project import Project as DockerComposeProject
from compose.cli.docker_client import docker_client
from compose.config.environment import Environment
from compose.config.types import VolumeSpec

from dockerpty.pty import PseudoTerminal, ExecOperation

class Runtime(object):

    def __init__(self):
        self.home_path = os.path.expanduser('~/.metal')
        self.installation_path = os.path.dirname(metal.__file__)

        self.installed_projects_file = self.home_path + '/installed_projects.json'
        self.active_projects_file = self.home_path + '/active_projects.json'
        self.docker_compose_file = self.home_path + '/docker-compose.yml'
        self.nginx_sites_path = self.home_path + '/nginx/sites/'

        self.__init_home()
        self.__load_projects()

    def install_project(self, project):
        project.installed = True
        self.installed_projects.append(project)
        self.__update_installed_projects()
        self.__rebuild_docker_compose()

    def activate_project(self, project):
        project.active = True
        self.active_projects.append(project)
        self.__update_active_projects()
        self.__add_project_site(project)

        compose_project = self.__get_docker_compose_project()
        compose_project.up([project.name], detached=True)

    def deactivate_project(self, project):
        project.active = False
        self.active_projects.remove(project)
        self.__update_active_projects()
        self.__remove_project_site(project)

        compose_project = self.__get_docker_compose_project()
        compose_project.stop([project.name])

    def restart_project(self, project):
        compose_project = self.__get_docker_compose_project()
        compose_project.restart([project.name])

    def build_project(self, project):
        # TODO install other dependencies (composer, npm, ...)
        compose_project = self.__get_docker_compose_project()
        service = compose_project.get_service('rails')

        compose_project.initialize()

        container = service.create_container(
            one_off=True,
            command='bundle install --path vendor/bundle',
            volumes=[VolumeSpec.parse(project.path + ':/app')]
        )

        container.start()

        for log in container.attach(stream=True, logs=True):
            sys.stdout.write(log)
            sys.stdout.flush()

        compose_project.client.remove_container(container.id, force=True, v=True)

    def open_shell(self, service_name):
        compose_project = self.__get_docker_compose_project()
        service = compose_project.get_service(service_name)

        container = service.get_container()
        exec_id = container.create_exec('sh -l', stdin=True, tty=True)
        pty = PseudoTerminal(
            compose_project.client,
            ExecOperation(
                compose_project.client,
                exec_id,
                interactive=True
            )
        )
        pty.start()

    def execute_command(self, service_name, command):
        compose_project = self.__get_docker_compose_project()
        service = compose_project.get_service(service_name)

        container = service.get_container()
        exec_id = container.create_exec('sh -l -c \"%s"' % command, stdin=True, tty=True)
        pty = PseudoTerminal(
            compose_project.client,
            ExecOperation(
                compose_project.client,
                exec_id,
                interactive=True
            )
        )
        pty.start()

    def sync_services(self):
        compose_project = self.__get_docker_compose_project()
        if len(self.active_projects) > 0:
            if len(compose_project.containers(['nginx'])) > 0:
                compose_project.restart(['nginx'])
            else:
                compose_project.up(['nginx'])
        else:
            compose_project.down(False, True)

    def get_project(self, name):
        for project in self.installed_projects:
            if project.name == name:
                return project

    def __get_docker_compose_project(self):
        client = docker_client(Environment())
        config_data = config.load(
            config.ConfigDetails(
                self.home_path,
                [
                    config.ConfigFile.from_filename(self.docker_compose_file)
                ]
            )
        )

        return DockerComposeProject.from_config(
            name='metal',
            client=client,
            config_data=config_data
        )

    def __add_project_site(self, project):

        with open(self.installation_path + '/nginx/project.conf') as f:
            project_site_config = f.read()
            project_site_config = project_site_config.replace('[PROJECT_NAME]', project.name)

        with open(self.nginx_sites_path + project.name + '.conf', 'w+') as f:
            f.write(project_site_config)

    def __remove_project_site(self, project):
        os.remove(self.nginx_sites_path + project.name + '.conf')

    def __update_installed_projects(self):
        with open(self.installed_projects_file, 'w+') as f:
            f.write(json.dumps(map(lambda project: project.serialize(), self.installed_projects)))

    def __update_active_projects(self):
        with open(self.active_projects_file, 'w+') as f:
            f.write(json.dumps(map(lambda project: project.name, self.active_projects)))

    def __rebuild_docker_compose(self):

        with open(self.installation_path + '/docker/docker-compose.base.yml') as f:
            docker_compose = f.read()

        with open(self.installation_path + '/docker/docker-compose.project.yml') as f:
            project_docker_compose = f.read()
            aliases_regex = re.compile(r'( +)\[ALIASES\]\n')
            for project in self.installed_projects:
                docker_compose = aliases_regex.sub('\\1- %s.test\n\\1[ALIASES]\n' % project.name, docker_compose) + \
                    project_docker_compose \
                        .replace('[PROJECT_NAME]', project.name) \
                        .replace('[PROJECT_PATH]', project.path)

        docker_compose = docker_compose \
            .replace('[INSTALLATION_PATH]', self.installation_path) \
            .replace('[HOME_PATH]', self.home_path)

        docker_compose = aliases_regex.sub('', docker_compose)

        with open(self.docker_compose_file, 'w+') as f:
            f.write(docker_compose)

    def __init_home(self):
        if (not os.path.exists(self.home_path)):
            os.makedirs(self.nginx_sites_path)
            copyfile(self.installation_path + '/nginx/default.conf', self.nginx_sites_path + 'default.conf')
            with open(self.installed_projects_file, 'w+') as f:
                f.write('[]')
            with open(self.active_projects_file, 'w+') as f:
                f.write('[]')

    def __load_projects(self):

        self.installed_projects = []
        with open(self.installed_projects_file) as f:
            for serialized_project in json.load(f):
                project = Project.deserialize(serialized_project)
                project.installed = True
                self.installed_projects.append(project)

        self.active_projects = []
        with open(self.active_projects_file) as f:
            active_project_names = json.load(f)
            for project in self.installed_projects:
                if project.name in active_project_names:
                    project.active = True
                    self.active_projects.append(project)
