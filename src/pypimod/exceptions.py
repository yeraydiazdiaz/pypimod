class PyPIModException(Exception):
    """Base class to all pypimod exceptions."""

    pass


class UninstallablePackageError(PyPIModException):
    pass


class PyPIAPIError(PyPIModException):
    pass


class PyPIWebError(PyPIModException):
    pass
