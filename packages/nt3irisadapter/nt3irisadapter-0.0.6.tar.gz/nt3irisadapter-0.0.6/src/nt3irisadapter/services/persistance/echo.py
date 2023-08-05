from ..model.pos_service_pb2 import Status, CheckServiceResponse, StatusType
from ..logic import helpers


def check_service() -> CheckServiceResponse:
    """
Check if service is running
    :return: CheckServiceResponse
    """
    try:
        # create CheckServiceResponse object
        status = Status(
            type=StatusType.OK,
            message="Service up and running"
        )
        response = CheckServiceResponse(
            status=status
        )
        return response
    except Exception as exception:
        helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
        return helpers.get_error_object(CheckServiceResponse, str(exception))
