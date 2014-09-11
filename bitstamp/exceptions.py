class ParametersError(Exception):
    """ Some parameters are wrong typed or not available. """


class MissingCredentials(Exception):
    """ Authentication credentials are missing. """
