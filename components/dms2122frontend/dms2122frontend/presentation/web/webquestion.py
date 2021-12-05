""" WebQuestion class module.
"""

from typing import Dict, List, Optional
from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils


class WebQuestion():
    """ Monostate class responsible of the question operation utilities.
    """
    @staticmethod
    def list_questions(backend_service: BackendService) -> List:
        """ Gets the list of questions from the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - List: A list of user data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.list_questions(session.get('token'))
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []

    @staticmethod
    def create_question(backend_service: BackendService, title: str,  body: str, option1: str, option2: str, 
            option3: str, correct_answer: int, punctuation: float, penalty: float) -> Optional[Dict]:
        """ Creates a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - Dict: A dictionary with the newly created question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.create_question(session.get('token'), title, body, option1, option2,
                        option3, correct_answer, punctuation, penalty)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def edit_question(backend_service: BackendService, id: int, title: str,  body: str, option1: str, option2: str, 
            option3: str, correct_answer: int, punctuation: float, penalty: float) -> Optional[Dict]:
        """ Edits a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - Dict: A dictionary with the edited question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.edit_question(session.get('token'), id, title, body, option1, option2,
                        option3, correct_answer, punctuation, penalty)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def get_question(backend_service: BackendService, id: int) -> Optional[Dict]:
        """ gets a question from the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - Dict: A dictionary with the newly created question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.get_question(session.get('token'), id)
        WebUtils.flash_response_messages(response)
        return response.get_content()


    @staticmethod
    def question_has_answers(backend_service: BackendService, id: id) -> bool:
        """ Updates the user roles in the authentication service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - bool: Whether the question has answers (`True`) or not (`False`)
        """
        response: ResponseData = backend_service.question_has_answers(session.get('token'), id)
        WebUtils.flash_response_messages(response)
        return response.is_successful()
