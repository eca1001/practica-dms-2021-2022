""" BackendConfiguration class module.
"""

from typing import Dict
from dms2122common.data.config import ServiceConfiguration


class BackendConfiguration(ServiceConfiguration):
    """ Class responsible of storing the backend service configuration.
    """

    #TODO: implement everything else


    def set_db_connection_string(self, db_connection_string: str) -> None:
        """ Sets the db_connection_string configuration value.

        Args:
            - db_connection_string: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['db_connection_string'] = str(db_connection_string)

    def get_db_connection_string(self) -> str:
        """ Gets the db_connection_string configuration value.

        Returns:
            - str: A string with the value of db_connection_string.
        """

        return str(self._values['db_connection_string'])

    #TODO: implement everything else
