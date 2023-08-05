from ..model.pos_service_pb2 import Status, StatusType, AuthorizeResponse, AuthorizeRequest, LoginRequest, \
    LoginResponse, LogoutRequest, LogoutResponse
from ..logic import helpers


def authorize(request: AuthorizeRequest):
    """
Authorize a POS device
    :param request: AuthorizeRequest
    :return: AuthorizeResponse
    """
    try:
        # create CheckServiceResponse object
        status = Status(
            type=StatusType.OK,
            message="OK"
        )
        response = AuthorizeResponse(
            status=status
        )
        return response
    except Exception as exception:
        helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
        return helpers.get_error_object(AuthorizeResponse, str(exception))


def login(request: LoginRequest):
    """
Login a POS device
    :param request: LoginRequest
    :return: LoginResponse
    """
    try:
        status = Status(
            type=StatusType.OK,
            message="OK"
        )
        response = LoginResponse(
            status=status
        )
        return response
    except Exception as exception:
        helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
        return helpers.get_error_object(LoginResponse, str(exception))


def logout(request: LogoutRequest):
    """
Logout a POS device
    :param request: LogoutRequest
    :return: LogoutResponse
    """
    try:
        status = Status(
            type=StatusType.OK,
            message="OK"
        )
        response = LogoutResponse(
            status=status
        )
        return response
    except Exception as exception:
        helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
        return helpers.get_error_object(LogoutResponse, str(exception))
