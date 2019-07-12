class Project(object):

    @staticmethod
    def deserialize(data):
        return Project(data['name'], data['path'], data['framework'])

    def __init__(self, name, path, framework, database = 'mysql'):
        self.name = name
        self.path = path
        self.framework = framework
        self.database = database

        self.installed = False
        self.active = False

    def serialize(self):
        return {
            'name': self.name,
            'path': self.path,
            'framework': self.framework,
        }
