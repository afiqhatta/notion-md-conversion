class publisherButton(object):

    def __init__(self, name, callBack):
        self.name = name
        self.callBack = callBack

    def generateButton(self):

        baseString = """
        $(function() {
                      $('a#{buttonName}').on('click', function(e) {
                        e.preventDefault()
                        $.getJSON('/{callback}',
                            function(data) {
                          //do nothing
                        });
                        return false;
                      });
                    });
        """
        return baseString.replace("{buttonName}", self.name).replace("{callback}", self.callBack)
