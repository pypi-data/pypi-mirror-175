import iris
import logging
import uuid
from concurrent import futures
import grpc
from ..model import pos_service_pb2_grpc as pos_grpc
from ..model.service_config import ServiceConfig
from ..model.pos_service_pb2 import Status, CheckServiceResponse, StatusType, LoginResponse, LogoutResponse, \
    AuthorizeResponse
from nt3core.logger import log
from nt3core.logger.log_context import ctx
from ..persistance import authorization, echo
from ..logic import helpers


# noinspection PyUnresolvedReferences,PyBroadException
class Listener(pos_grpc.POSServicer):

    def __init__(self, service_config: ServiceConfig) -> None:
        """
    Initialize the grpc listener
        :param service_config: ServiceConfig object containing the service specific settings
        """
        # store configs
        self._api_name = "IRIS Adapter"
        self._service_config = service_config
        try:
            super().__init__()
        except Exception as exception:
            helpers.log_iris("Error", f"Error initializing the IRIS Adapter grpc listener: {exception}", "")

    # region Methods from requests

    def CheckService(self, request, context):
        """
    Checks if the IRIS Adapter service is running, triggered by the grpc server
        :param request: sent by the grpc server
        :param context: sent by the grpc server
        """
        # generate trace id for request
        ctx.trace_id = str(uuid.uuid4())
        try:
            # log request message
            helpers.log_iris("Debug", "CheckService|IN|Request received", ctx.trace_id)
            response = echo.check_service()

            # log response message
            helpers.log_iris("Debug", f"CheckPartner|OUT|\n{response}", ctx.trace_id)
            return response
        except Exception as exception:
            helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
            return helpers.get_error_object(CheckServiceResponse, str(exception))

    # endregion

    def Authorize(self, request, context):
        """
    Authorize a POS device
        :param request: sent by the grpc server
        :param context: sent by the grpc server
        """
        # generate trace id for request
        ctx.trace_id = str(uuid.uuid4())

        try:
            # log request message
            helpers.log_iris("Debug", f"Authorize|IN|\n{request}", ctx.trace_id)

            response = authorization.authorize(request)

            # log response message
            helpers.log_iris("Debug", f"Authorize|OUT|\n{response}", ctx.trace_id)
            return response
        except Exception as exception:
            helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
            return helpers.get_error_object(AuthorizeResponse, str(exception))

    def Login(self, request, context):
        """
    Login a POS device
        :param request: sent by the grpc server
        :param context: sent by the grpc server
        """
        # generate trace id for request
        ctx.trace_id = str(uuid.uuid4())

        try:
            # log request message
            helpers.log_iris("Debug", f"Login|IN|\n{request}", ctx.trace_id)

            response = authorization.login(request)

            # log response message
            helpers.log_iris("Debug", f"Login|OUT|\n{response}", ctx.trace_id)
            return response
        except Exception as exception:
            helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
            return helpers.get_error_object(LoginResponse, str(exception))

    def Logout(self, request, context):
        """
    Logout a POS device
        :param request: sent by the grpc server
        :param context: sent by the grpc server
        """
        # generate trace id for request
        ctx.trace_id = str(uuid.uuid4())

        try:
            # log request message
            helpers.log_iris("Debug", f"Logout|IN|\n{request}", ctx.trace_id)

            response = authorization.logout(request)

            # log response message
            helpers.log_iris("Debug", f"Logout|OUT|\n{response}", ctx.trace_id)
            return response
        except Exception as exception:
            helpers.log_iris("Error", f"Error: {exception}", ctx.trace_id)
            return helpers.get_error_object(LogoutResponse, str(exception))


class Server:

    def __init__(self, service_config: ServiceConfig) -> None:
        """
    Initialize grpc server
        :param service_config: ServiceConfig object containing the service specific settings
        """
        # initialize logger
        self._logger_app = logging.getLogger("application")
        self._logger_comm = logging.getLogger("communication")

        # store configs
        self._service_config = service_config
        self._api_name = "IRIS Adapter"
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    def serve(self):
        """
    Starts the grpc server
        """
        try:
            pos_grpc.add_POSServicer_to_server(
                Listener(service_config=self._service_config),
                self.server)
            helpers.log_iris("Info", f"Starting {self._api_name} grpc server on port {self._service_config.port_grpc}",
                             "")
            self.server.add_insecure_port(f"[::]:{self._service_config.port_grpc}")
            self.server.start()
            self.server.wait_for_termination()
        except Exception as exception:
            raise exception

    def stop(self):
        """
    Stops the server
        """
        self.server.stop(0)
