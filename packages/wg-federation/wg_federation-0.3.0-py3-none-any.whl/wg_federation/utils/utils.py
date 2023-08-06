from typing import Any


class Utils:
    """
    Contains reusable utility code.
    This class only contains short, static methods.
    """

    @staticmethod
    def classname(instance: object) -> str:
        """
        Display the class name of a given object instance
        :param instance: Instance to get the class from
        :return:
        """
        return f'{instance.__class__.__name__}♦'

    @staticmethod
    def always_dict(instance: Any) -> dict:
        """
        Takes any argument. Returns it unmodified if it’s a, otherwise, return empty dict
        :param instance: anything
        :return: instance if instance is dict, otherwise {}
        """
        if not isinstance(instance, dict):
            return {}

        return instance
