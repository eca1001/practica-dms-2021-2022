""" REST API controllers responsible of handling the question operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from flask import current_app, session
from dms2122backend.data.db.exc import QuestionExistsError
from dms2122backend.data.db.results import Question
from dms2122backend.service import QuestionsServices
from dms2122backend.data.rest.authservice import AuthService
from dms2122common.data.rest import ResponseData

def list_questions() -> Tuple[List[Dict], Optional[int]]:
    """Lists the existing questions.

    Returns:
        - Tuple[List[Dict], Optional[int]]: A tuple with a list of dictionaries for the questions' data
          and a code 200 OK.
    """
    with current_app.app_context():
        questions: List[Dict] = QuestionsServices.list_questions(current_app.db)
    return (questions, HTTPStatus.OK.value)

def create_question(authservice: AuthService, body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Creates a question if the requestor has the Teacher role.

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
            question: Dict = QuestionsServices.create_question(
                body['title'], body['body'],  body['option1'], body['option2'], body['option3'], body['correct_answer'], body['punctuation'],body['penalty'],current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionExistsError:
            return ('A question with the same title already exists', HTTPStatus.CONFLICT.value)
    return (question, HTTPStatus.OK.value)

def get_question(authservice: AuthService, body: Dict, token_info: Dict) -> Tuple[Union[Optional[Question], str], Optional[int]]:
    """Creates a question if the requestor has the Teacher role.

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
            question = QuestionsServices.get_question(
                body['title'], body['body'],  body['option1'], body['option2'], body['option3'], body['correct_answer'], body['punctuation'],body['penalty'],current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (question, HTTPStatus.OK.value)

def get_question_by_id(id: int, token_info: Dict) -> Tuple[Union[Optional[Question], str], Optional[int]]:
    """Creates a question if the requestor has the Teacher role.

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
        try:
            question = QuestionsServices.get_question_by_id(
                id, current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (question, HTTPStatus.OK.value)

