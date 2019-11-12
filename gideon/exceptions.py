
class GideonError(Exception):
    pass


class NonExistsField(GideonError):
    pass


class PrivateField(GideonError):
    pass


class InvalidChoice(GideonError):
    pass
