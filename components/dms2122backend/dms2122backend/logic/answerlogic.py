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
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.resultsets import Questions


class AnswerLogic():
    """ Monostate class that provides logic-level operations to handle answer-related use cases.
    """
    @staticmethod
    def create(auth_service: AuthService, session: Session, user: str, number: int, id: int, token_info: Dict) -> Answer:
        """ Creates a new answer record.

        Note:
            Any existing transaction will be committed.

        Args:
            - auth_service (AuthService): the authentication service
            - token_info (Dict): A dictionary of information provided by the security schema handlers.
            - session (Session): The session object.
            - user (str): The user name string.
            - number (int): Answer's selection number by the student.
            - id (int): Id of the question.

        Returns:
            - Answer: The created `Answer` result.
        """
        '''response: ResponseData = auth_service.get_user_has_role(session.get('token'), 
                                                token_info['user_token']['user'], "Student")
        if response.is_successful() == False:
            raise ForbiddenOperationError'''
        try:
            new_answer: Answer = Answers.answer(session, user, number, id)
        except Exception as ex:
            raise ex
        return new_answer
    
    @staticmethod
    def list_all(session: Session) -> List[Answer]:
        """Lists every question.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Question]: A list of `Question` registers.
        """
        return Answers.list_all(session)

    @staticmethod
    def list_all_for_user(session: Session,user: str) -> List[Answer]:
        """Lists the existing questions.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.

        Returns:
            - List[Answer]: A list of Answer with the answers' data.
        """
        try:
            return Answers.list_all_for_user(session, user)
        except Exception as ex:
            raise ex

    @staticmethod
    def list_all_for_question(session: Session, id: int) -> List[Answer]:
        """Lists the existing questions.

        Args:
            - session (Session): The session object.
            - questionId (int): Id of the question.

        Returns:
            - List[Answer]: A list of Answer with the answers' data.
        """
        try:
            return Answers.list_all_for_question(session, id)
        except Exception as ex:
            raise ex        

    @staticmethod
    def question_has_answers(auth_service: AuthService, token_info: Dict, session: Session,id: int) -> bool:
        """Return True or False if a certain question has answers.

        Args:
            - auth_service (AuthService): the authentication service
            - token_info (Dict): A dictionary of information provided by the security schema handlers.
            - session (Session): The session object.
            - questionId (int): Id of the question.

        Returns:
            - bool: True if question has answers, False if not
        """
        response: ResponseData = auth_service.get_user_has_role(session.get('token'), 
                                                token_info['user_token']['user'], "Teacher")
        if response.is_successful() == False:
            raise ForbiddenOperationError
        try:
            return Answers.question_has_answers(session,id)
        except Exception as ex:
            raise ex        


    @staticmethod
    def get_answer(session: Session ,user: str, id: int) -> Answer:
        """Return a answer of a certain question and user.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.
            - id (int): The question id.

        Returns:
            - Answer: The Answer of the question.
        """
        try:
            answer: Answer = Answers.get_answer(session,user,id)
        except Exception as ex:
            raise ex
        return answer

    @staticmethod
    def answer_punctuation(session: Session,answer:Answer)->Optional[float]:
        try:
            question: Optional[Question] = Questions.get_question_by_id(session,answer.id)
            if question is not None:
                if question.correct_answer==answer.number:
                    return question.punctuation
                return -question.penalty
            return None
        except Exception as ex:
            raise ex

