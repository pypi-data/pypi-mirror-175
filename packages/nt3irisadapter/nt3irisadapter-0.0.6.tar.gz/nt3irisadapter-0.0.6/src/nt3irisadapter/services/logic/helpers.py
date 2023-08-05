import iris
from ..model.pos_service_pb2 import Status, StatusType


# noinspection PyCallingNonCallable
def get_error_object(response_object: object, message: str) -> str:
    """
Generates an error object
    :param response_object: Response object used for the error response
    :param message: Status message
    :return: Error response object
    """
    status = Status(
        type=StatusType.ERROR,
        message=str(message)
    )
    return response


def log_iris(log_type: str, message: str, trace_id: str = ""):
    """
Logs the message in IRIS
    :param log_type: Log type
    :param message: Message
    :param trace_id: Trace id
    :return:
    """
    print(f"{log_type} - {message}")
    iris.cls("NovaTouch.Logic.Adapter").Log(log_type, message, trace_id)
