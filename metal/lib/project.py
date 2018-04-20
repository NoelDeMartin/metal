class Project(object):

    @staticmethod
    def deserialize(data):
        return Project(data['name'], data['path'])

    def __init__(self, name, path):
        self.name = name
        self.path = path

        self.installed = False
        self.active = False

    def serialize(self):
        return { 'name': self.name, 'path': self.path }
