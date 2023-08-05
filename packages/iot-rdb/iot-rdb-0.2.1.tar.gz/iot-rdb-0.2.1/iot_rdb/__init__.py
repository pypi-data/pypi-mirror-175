# Parsing every util class for redis connection
from iot_rdb.util import IotRedisBasic
from iot_rdb.util import IotRedisPublisher
from iot_rdb.util import IotRedisSubscriber
from iot_rdb.util import IotRedisPubSub
__version__ = "0.2.1"


class IotRedisCommon:
    """Common variable to all containers

    This standard is for defining all PubSub clients
    in every container to be created.

    class CrossConnection:
        "container_name" = (tuple with channels to listen)
        "container_name2" = ()
        ...
    }

    Channels publishing now:
        - CONTROLLER : control_input, init_vars
        - OPCUA: raw_outputs, perturbations, inputs, set_points
        - AUTOENCODER: filtered_outputs, init_vars
        - DB:
        - DBDRIVER:
        - MANAGER:
    """

    class CrossConnection:
        OPCUA = ("control_input", "init_vars")
        CONTROLLER = ("raw_outputs", "perturbations", "filtered_outputs", "inputs", "set_points")
        AUTOENCODER = ("raw_outputs", "perturbations", "inputs")
        DB = ("raw_outputs", "filtered_outputs", "perturbations", "inputs", "set_points")
        DBDRIVER = ("raw_outputs", "filtered_outputs", "perturbations", "inputs", "set_points")
