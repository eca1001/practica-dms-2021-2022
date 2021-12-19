""" WebStats class module.
"""

from typing import Dict, List, Optional
from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils


class WebStats():
    """ Monostate class responsible of the statistics operation utilities.
    """

    @staticmethod
    def user_stats(backend_service: BackendService, username: str) -> Optional[Dict]:
        """ Get a user's stats.

        Args:
            - backend_service (BackendService): The backend service.
            - username (str): the user's name

        Returns:
            - Dict: A dictionary of statistics data dictionaries (the dict may be empty)
        """
        response: ResponseData = backend_service.user_stats(session.get('token'), username)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def question_stats(backend_service: BackendService) -> Optional[Dict]:
        """ Get a question's stats.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - Dict: A dictionary of statistics data dictionaries (the dict may be empty)
        """
        response: ResponseData = backend_service.question_stats(session.get('token'))
        WebUtils.flash_response_messages(response)
        return response.get_content()