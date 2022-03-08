from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )


class ServerError(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Error on the server side.
        """
        status_code = 500
        super().__init__(status_code, context)


class NotFound(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Item not found.
        """
        status_code = 404
        super().__init__(status_code, context)


class RequiresAuth(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Reading of the item requires auth.
        """
        status_code = 401
        super().__init__(status_code, context)


class PermissionDenied(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Reading of the item requires special permissions.
        """
        status_code = 403
        super().__init__(status_code, context)


class InvalidRequest(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Received request is invalid.
        """
        status_code = 400
        super().__init__(status_code, context)
