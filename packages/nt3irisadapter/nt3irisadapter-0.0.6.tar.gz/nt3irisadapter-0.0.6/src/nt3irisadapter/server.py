from nt3core.logger import logger_config
from .services.model.service_config import ServiceConfig
from .services.server_grpc.server_grpc import Server
import iris


def run(port: int, timeout: int):
    # load configuration files
    print(f"Reparing to run IRIS adapter on port {port} with timeout {timeout}...")
    print(f"Create service config class")
    service_config = ServiceConfig(port_grpc=port, timeout=timeout)
    print(f"Create gRpc Server class")
    server = Server(service_config=service_config)
    print(f"Start gRpc Server")
    server.serve()


if __name__ == "__main__":
    run(31351, 3)
