class Participant:
    def __init__(self, **kwargs):
         self._fname = kwargs['fname']
         self._lname = kwargs['lname']
         self._birthday = kwargs['birthday']
         self._sex = kwargs['sex']
         self._level = kwargs['level']

    @property
    def _fname(self):
        return self._fname

    @_fname.setter
    def _fname(self, value):
        self._fname = value

    @property
    def _lname(self):
        return self._lname

    @_lname.setter
    def _lname(self, value):
        self._lname = value

    @property
    def _birthday(self):
        return self._birthday

    @_birthday.setter
    def _birthday(self, value):
        self._birthday = value

    @property
    def _sex(self):
        return self._sex

    @_sex.setter
    def _sex(self, value):
        self._sex = value

    @property
    def _level(self):
        return self._level

    @_level.setter
    def _level(self, value):
        self._level = value
