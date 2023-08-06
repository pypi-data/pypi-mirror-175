from ipaddr import IPNetwork
from pydantic import BaseModel, validator

from wg_federation.data.state.federation import Federation
from wg_federation.data.state.wireguard_interface import WireguardInterface


# mypy: ignore-errors
# https://github.com/pydantic/pydantic/issues/156


class State(BaseModel, frozen=True):
    """
    Data class representing a full configuration file
    Important: https://pydantic-docs.helpmanual.io/usage/models/#field-ordering
    """

    federation: Federation
    interfaces: dict[str, WireguardInterface]

    # pylint: disable=no-self-argument
    @validator('interfaces')
    def wireguard_interface_are_valid(
            cls, value: dict[str, WireguardInterface], values: dict
    ) -> dict[str, WireguardInterface]:
        """
        Validate interfaces
        :param value: interfaces value
        :param values: other validated attributes of the current object as dict
        :return:
        """
        interface_names = []
        interface_addresses = []
        interface_listen_ports = []
        for wireguard_interface in value.values():
            if wireguard_interface.name in interface_names:
                raise ValueError(
                    f'The wireguard interface “{wireguard_interface.name}” has the same name of another interface.'
                )

            for address in wireguard_interface.addresses:
                for other_address in interface_addresses:
                    if IPNetwork(str(address)).overlaps(other_address):
                        raise ValueError(
                            f'The wireguard interface address “{wireguard_interface.name}”'
                            f' has an address “{address}” that overlaps with another address: “{other_address}”.'
                        )

                interface_addresses.append(IPNetwork(str(address)))

            if wireguard_interface.listen_port in interface_listen_ports:
                raise ValueError(
                    f'The wireguard interface “{wireguard_interface.name}” has the same listen_port'
                    f' “{wireguard_interface.listen_port}” as another interface.'
                )

            if values.get('federation').port_within_forum_range(wireguard_interface.listen_port):
                raise ValueError(
                    f'The wireguard interface “{wireguard_interface.name}” has a listen_port '
                    f'“{wireguard_interface.listen_port}” within the range of the forum ports.'
                )

            if values.get('federation').port_within_phone_line_range(wireguard_interface.listen_port):
                raise ValueError(
                    f'The wireguard interface “{wireguard_interface.name}” has a listen_port '
                    f'“{wireguard_interface.listen_port}” within the range of the phone line ports.'
                )

            interface_names.append(wireguard_interface.name)
            interface_listen_ports.append(wireguard_interface.listen_port)
        return value

    def to_yaml_ready_dict(self) -> dict:
        """
        Return a dict version of this object, ready to be serialized in a configuration file
        :return:
        """
        return dict(self.copy(update={
            'interfaces': {key: dict(interface.to_yaml_ready_dict()) for key, interface in self.interfaces.items()},
            'federation': self.federation.to_yaml_ready_dict()
        }))
