""" Main class """
from deepmerge import always_merger

from wg_federation.controller.controller_dispatcher import ControllerDispatcher
from wg_federation.data.state.federation import Federation
from wg_federation.data.state.state import State
from wg_federation.data.state.wireguard_interface import WireguardInterface
from wg_federation.data_transformation.loader.file.yaml_file_configuration_loader import YamlFileConfigurationLoader
from wg_federation.di.container import Container
from wg_federation.input.manager.input_manager import InputManager
import yaml


class Main:
    """ Main """

    _container: Container = None

    def __init__(self, container: Container = None):
        """
        Constructor
        """
        if self._container is None:
            self._container = container or Container()

        self._container.wire(modules=[__name__])

    def main(self) -> int:
        """ main """
        input_manager: InputManager = self._container.input_manager()
        controller_dispatcher: ControllerDispatcher = self._container.controller_dispatcher()

        user_input = input_manager.parse_all()
        controller_dispatcher.dispatch_all(user_input)

        # configuration_loader = self._container.configuration_loader()
        # print(configuration_loader.load(YamlFileConfigurationLoader.get_supported_source(), ('.pre-commit-config.yaml',)))

        # ok = WireguardInterfaceConfig(
        #     name='toto',
        #     server_private_key='L9kYW/Kej96/L4Ae2lK50X46gJMfrplRAY4WbK0w4iYRE=',
        #     server_public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
        #     listen_port=35233,
        #     mtu=68,
        #     # dns=['1.1.1.1'],
        #     addresses=['10.10.100.1/24'],
        # )
        # ok2 = WireguardInterfaceConfig(
        #     name='tata',
        #     server_private_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4iYRE=',
        #     server_public_key='L9kYW/Kej96/L4Ae2lK5X46gJMfrplRAY4WbK0w4YRE=',
        #     listen_port=35243,
        #     mtu=68,
        #     # dns=['1.1.1.1'],
        #     addresses=['10.10.10.1'],
        # )
        # federation = FederationConfig(
        #     name="tartzepaezai",
        #     forum_min_port=64900,
        #     forum_max_port=65000,
        # )
        # wir = MainConfig(federation=federation, interfaces={'federation0': ok, 'federation1': ok2})
        # # wir.interfaces.update({})
        #
        #
        # print('-----------------------')
        #
        # with open('test.yaml', 'a+') as fp:
        #     fp.seek(0)
        #     data = yaml.safe_load(fp)
        #
        #     if None is data:
        #         data = {}
        #
        #     print(data)
        #     print('-----------------------')
        #
        #     print(wir.to_yaml_ready_dict())
        #
        #     data.update(wir.to_yaml_ready_dict())
        #
        # with open('test.yaml', 'w') as fp:
        #     yaml.dump(data, fp)
        #
        # print('-----------------------')
        # print(data)
        return 0
