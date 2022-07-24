from publisherButton import publisherButton


class PublisherButtonGenerator(object):

    def __init__(self, names: list, callbacks: list):
        self.names = names
        self.callbacks = callbacks

    def getNameCallbackDict(self):
        return dict(zip(self.names, self.callbacks))

    def getList(self):
        return [publisherButton(name, callback).generateButton() for
                name, callback in self.getNameCallbackDict().items()]

    def getJSstring(self):
        return " ".join(self.getList())

    def getWrapInJavascipt(self):
        return '<script type=text/javascript>' + self.getJSstring() + '</script>'
