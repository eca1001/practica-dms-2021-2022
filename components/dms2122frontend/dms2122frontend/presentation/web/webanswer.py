""" WebAnswer class module.
"""

from typing import Dict, List, Optional
from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils

class WebAnswer():
    """ Monostate class responsible of the question operation utilities.
    """

    @staticmethod
    def answer_question(backend_service: BackendService, id: int, number: int, username: str) -> Optional[Dict]:
        """ Answer a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - id: Question id
            - number: Number of the selected answer
            - username: Students' username

        Returns:
            - Dict: A dictionary with the newly created answer if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.answer_question(session.get('token'), id, number, username)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def list_all_for_question(backend_service: BackendService, id: int) -> Optional[List]:
        """ Gets the list of users from the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - id (int): the question's id

        Returns:
            - List: A list of answer data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.list_all_for_question(session.get('token'), id)
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []

    @staticmethod
    def list_all_for_user(backend_service: BackendService, username: str) -> Optional[List]:
        """ Gets the list of users from the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - username (str): the user's name

        Returns:
            - List: A list of answer data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.list_all_for_user(session.get('token'), username)
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []
    
    @staticmethod
    def get_answer(backend_service: BackendService, username: str, id: int) -> Optional[Dict]:
        """ Return an answer a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - id: Question id
            - number: Number of the correct answer
            - username: Students' username

        Returns:
            - Dict: A dictionary with the newly created question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.get_answer(session.get('token'), username, id)
        WebUtils.flash_response_messages(response)
        return response.get_content()