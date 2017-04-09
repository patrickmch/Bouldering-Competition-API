class Participant:
    def __init__(self, **kwargs):
         self.props = kwargs

    def set_prop(self, key, value):
        self.variables[key] = value

    def get_prop(self, key):
        return self.props.get(var, none)


jerry = Participant()

jerry.name = "jerry l"
