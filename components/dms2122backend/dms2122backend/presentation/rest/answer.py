""" REST API controllers responsible of handling the question operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from flask import current_app, session
from dms2122backend.data.db.exc import QuestionExistsError
from dms2122backend.service import AnswersServices
from dms2122backend.data.rest.authservice import AuthService
from dms2122common.data.role import Role
from dms2122common.data.rest import ResponseData

def answer(authservice: AuthService, body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Answer a question if the requestor has the Student role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the question.
            - 409 CONFLICT if an existing user already has all or part of the unique user's data.
    """
    with current_app.app_context():
        response: ResponseData = authservice.get_user_has_role(session.get('token'), token_info['user_token']['user'], "Student")
        if response.is_successful() == False:
            return (
                'Current user has not enough privileges to create a question',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            AnswersServices.answer(
                body['session'], body['username'],  body['number'], body['questionId']
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
    return (None, HTTPStatus.OK.value)


def list_all_for_user(authservice: AuthService, body: Dict, token_info: Dict) -> Tuple[Union[List[str], str], Optional[int]]:
    """List all question of an specific user if the requestor has the Student role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the question.
            - 409 CONFLICT if an existing user already has all or part of the unique user's data.
    """
    with current_app.app_context():
        response: ResponseData = authservice.get_user_has_role(session.get('token'), token_info['user_token']['user'], "Student")
        if response.is_successful() == False:
            return (
                'Current user has not enough privileges to create a question',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            answer: List[str] = AnswersServices.list_all_for_user(
                body['user'], current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (answer, HTTPStatus.OK.value)


def list_all_for_question(authservice: AuthService, body: Dict, token_info: Dict) -> Tuple[Union[List[str], str], Optional[int]]:
    """List all answers of an specific question if the requestor has the Teacher role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the question.
            - 409 CONFLICT if an existing user already has all or part of the unique user's data.
    """
    with current_app.app_context():
        response: ResponseData = authservice.get_user_has_role(session.get('token'), token_info['user_token']['user'], "Teacher")
        if response.is_successful() == False:
            return (
                'Current user has not enough privileges to create a question',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            answer: List[str] = AnswersServices.list_all_for_question(
                body['id'], current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (answer, HTTPStatus.OK.value)

def question_has_answers(authservice: AuthService, body: Dict, token_info: Dict) -> Tuple[bool, Optional[int]]:
    """List all answers of an specific question if the requestor has the Teacher role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the question.
            - 409 CONFLICT if an existing user already has all or part of the unique user's data.
    """
    with current_app.app_context():
        response: ResponseData = authservice.get_user_has_role(session.get('token'), token_info['user_token']['user'], "Teacher")
        if response.is_successful() == False:
            return (
                'Current user has not enough privileges to create a question',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            answer = AnswersServices.question_has_answers(
                body['id'], current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (answer, HTTPStatus.OK.value)