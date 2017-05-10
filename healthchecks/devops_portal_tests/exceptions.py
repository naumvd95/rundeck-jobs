class CustomBaseException(Exception):
    """Custom exception"""

    message = "An unknown exception occurred"

    def __init__(self, **kwargs):
        super(CustomBaseException, self).__init__()
        try:
            self._err_string = self.message % kwargs
        except Exception:
            self._err_string = self.message

    def __str__(self):
        return self._err_string


class SSHTimeout(CustomBaseException):

    message = ("Connection to the %(host)s via SSH timed out.\n"
               "User: %(user)s, Password: %(password)s")


class SSHExecCommandFailed(CustomBaseException):

    message = ("Command '%(command)s', exit status: %(exit_status)d, "
               "stderr:\n%(stderr)s\n"
               "stdout:\n%(stdout)s")


class SSHConnectionFailed(CustomBaseException):

    message = ("Connection to the %(host) failed\n"
               "User: %(user)s, Password: %(password)s")
