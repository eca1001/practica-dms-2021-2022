""" AnswerLogic class module.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema 
from dms2122backend.data.rest import AuthService
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.resultsets import Answers
from dms2122backend.logic.exc.forbiddenoperationerror import ForbiddenOperationError
from dms2122common.data.rest import ResponseData

class AnswerLogic():
    """ Monostate class that provides logic-level operations to handle answer-related use cases.
    """
    @staticmethod
    def create(auth_service: AuthService, token_info: Dict, session: Session, user: str, number: int, id: int) -> Answer:
        """ Creates a new answr record.

        Note:
            Any existing transaction will be committed.

        Args:
            - auth_service (AuthService): the authentication service
            - session (Session): The session object.
            - user (str): 
            - number (int):
            - id (int):


        Raises:
            - ValueError: If any field is empty.

        Returns:
            - Answer: The created `Answer` result.
        """
        response: ResponseData = auth_service.get_user_has_role(session.get('token'), 
                                                token_info['user_token']['user'], "Student")
        if response.is_successful() == False:
            raise ForbiddenOperationError
        try:
            new_answer: Answer = Answers.answer(session, user, number, id)
        except Exception as ex:
            raise ex
        return new_answer

    def list_all_for_user(session: Session,user: str) -> List[Answer]:
        """
        """
        return Answers.list_all_for_user(session, user)

    def list_all_for_question(session: Session,id: int) -> List[Answer]:
        """
        """
        return Answers.list_all_for_question(session, id)

    def question_has_answers(auth_service: AuthService, token_info: Dict,session: Session,id: int) -> bool:
        """
        """
        response: ResponseData = auth_service.get_user_has_role(session.get('token'), 
                                                token_info['user_token']['user'], "Teacher")
        if response.is_successful() == False:
            raise ForbiddenOperationError
        return Answers.question_has_answers(session,id)

    def get_answer(session: Session ,user: str, id: int) -> Answer:
        """
        """
        try:
            answer: Answer = Answers.get_answer(session,user,id)
        except Exception as ex:
            raise ex
        return answer

