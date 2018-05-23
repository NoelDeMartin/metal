import os
import re
import json
import metal

from .docker import Docker
from .project import Project

from shutil import copyfile

class Runtime(object):

    def __init__(self):
        self.home_path = os.path.expanduser('~/.metal')
        self.installation_path = os.path.dirname(metal.__file__)

        self.installed_projects_file = self.home_path + '/installed_projects.json'
        self.active_projects_file = self.home_path + '/active_projects.json'
        self.docker_compose_file = self.home_path + '/docker-compose.yml'
        self.nginx_sites_path = self.home_path + '/nginx/sites/'

        self.docker = Docker(self.home_path, self.docker_compose_file)

        self.__init_home()
        self.__load_projects()

    def install_project(self, project):
        project.installed = True
        self.installed_projects.append(project)
        self.__update_installed_projects()
        self.__rebuild_docker_compose()

    def uninstall_project(self, project):
        project.installed = False
        self.installed_projects.remove(project)
        self.__update_installed_projects()
        self.__rebuild_docker_compose()

    def activate_project(self, project):
        project.active = True
        self.active_projects.append(project)
        self.__update_active_projects()
        self.__add_project_site(project)
        self.docker.up([project.name])

    def deactivate_project(self, project):
        project.active = False
        self.active_projects.remove(project)
        self.__update_active_projects()
        self.__remove_project_site(project)
        self.docker.stop([project.name])

    def restart_project(self, project):
        self.docker.restart([project.name])

    def build_project(self, project):
        # TODO install other dependencies (npm, ...)

        build_commands = {
            'laravel': 'composer install',
            'rails': 'bundle install --path vendor/bundle',
        }

        self.docker.execute_command(
            project.framework,
            build_commands[project.framework],
            volumes=[project.path + ':/app'],
            one_off=True,
        )

    def open_shell(self, service_name):
        self.docker.open_shell(service_name)


    def execute_command(self, service_name, command):
        self.docker.execute_command(service_name, 'sh -l -c \"%s"' % command)

    def sync_services(self):
        if len(self.active_projects) > 0:
            if len(self.docker.get_containers(['nginx'])) > 0:
                self.docker.restart(['nginx'])
            else:
                self.docker.up(['nginx'])
        else:
            self.docker.down()

    def get_project(self, name):
        for project in self.installed_projects:
            if project.name == name:
                return project

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

        with \
            open(self.installation_path + '/docker/docker-compose.laravel.yml') as f_laravel, \
            open(self.installation_path + '/docker/docker-compose.rails.yml') as f_rails:
                projects_docker_compose = {
                    'laravel': f_laravel.read(),
                    'rails': f_rails.read(),
                }
                aliases_regex = re.compile(r'( +)\[ALIASES\]\n')
                for project in self.installed_projects:
                    docker_compose = aliases_regex.sub('\\1- %s.test\n\\1[ALIASES]\n' % project.name, docker_compose) + \
                        projects_docker_compose[project.framework] \
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
