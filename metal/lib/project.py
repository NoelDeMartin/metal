class Project(object):

    @staticmethod
    def deserialize(data):
        return Project(data['name'], data['path'], data['framework'])

    def __init__(self, name, path, framework):
        self.name = name
        self.path = path
        self.framework = framework

        self.installed = False
        self.active = False

    def serialize(self):
        return {
            'name': self.name,
            'path': self.path,
            'framework': self.framework,
        }
