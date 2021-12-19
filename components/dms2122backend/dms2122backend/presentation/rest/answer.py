""" REST API controllers responsible of handling the question operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from flask import current_app, session
from dms2122backend.data.db.exc import QuestionExistsError
from dms2122backend.service import AnswersServices
from dms2122backend.data.db.results.answer import Answer
from dms2122backend.data.rest.authservice import AuthService
from dms2122common.data.role import Role
from dms2122common.data.rest import ResponseData
from dms2122backend.data.db.exc.questionorusernotfounderror import QuestionOrUserNotFoundError
from dms2122backend.logic.exc.forbiddenoperationerror import ForbiddenOperationError

def answer(id: int, username: str, body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Answer a question if the requestor has the Student role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - TupleUnion[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to answer the question.
            - 404 NOT FOUND if an user or question does not exist.
    """
    with current_app.app_context():            
        try:
            answer = AnswersServices.answer(current_app.authservice,
                body['username'],  body['number'], body['id'], current_app.db, token_info
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionOrUserNotFoundError:
            return ('Question or User does not exist', HTTPStatus.NOT_FOUND.value)
        except ForbiddenOperationError:
            return (
                'Current user has not enough privileges to create a question',
                HTTPStatus.FORBIDDEN.value
            )
    return (answer, HTTPStatus.OK.value)


def list_all_for_user(username: str) -> Tuple[Union[List[Dict], str], Optional[int]]:
    """List all question of an specific user if the requestor has the Student role.

    Args:
        - username: A string with the Students' name
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[List[Dict], str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
    """
    with current_app.app_context():
        try:
            answers: List[Dict] = AnswersServices.list_all_for_user(username, current_app.db)
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (answers, HTTPStatus.OK.value)

def list_answers() -> Tuple[List[Dict], Optional[int]]:
    """Lists the existing questions.

    Returns:
        - Tuple[List[Dict], Optional[int]]: A tuple with a list of dictionaries for the questions' data
          and a code 200 OK.
    """
    with current_app.app_context():
        answers: List[Dict] = AnswersServices.list_answers(current_app.db)
    return (answers, HTTPStatus.OK.value)

def list_all_for_question(id: int) -> Tuple[Union[List[Dict], str], Optional[int]]:
    """List all answers of an specific question if the requestor has the Teacher role.

    Args:
        - id: Question id
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[List[Dict], str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
    """
    with current_app.app_context():
        try:
            answers: List[Dict] = AnswersServices.list_all_for_question(
                id, current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (answers, HTTPStatus.OK.value)

def question_has_answers( questionId: int, token_info: Dict) -> Tuple[Union[bool,str], Optional[int]]:
    """List all answers of an specific question if the requestor has the Teacher role.

    Args:
        - questionId: Question id
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[bool, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to answer the question.
    """
    with current_app.app_context():
        try:
            answer = AnswersServices.question_has_answers(current_app.authservice, token_info,
                questionId, current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)  
        except ForbiddenOperationError:
            return (
                'Current user has not enough privileges to create a question',
                HTTPStatus.FORBIDDEN.value
            )
    return (answer, HTTPStatus.OK.value)

def get_answer(username: str, id: int) -> Tuple[Union[Dict, str], Optional[int]]:
    """Return the answer of an specific question and user.

    Args:
        - username: A string with the Students' name
        - id: Question id
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
    """
    with current_app.app_context():
        try:
            answer: Dict = AnswersServices.get_answer(
                username, id, current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (answer, HTTPStatus.OK.value)

