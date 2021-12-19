""" QuestionLogic class module.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema 
from dms2122backend.data.rest import AuthService
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.resultsets import Questions
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.resultsets import Answers
from dms2122backend.logic.exc.forbiddenoperationerror import ForbiddenOperationError
from dms2122common.data.rest import ResponseData

class QuestionLogic():
    """ Monostate class that provides logic-level operations to handle question-related use cases.
    """


    @staticmethod
    def create(auth_service: AuthService, token_info: Dict, session: Session, title: str,  body: str, option1: str, 
                    option2: str, option3: str, correct_answer: int, punctuation: float, penalty: float) -> Question:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
            - auth_service (AuthService): the authentication service
            - token_info (Dict): A dictionary of information provided by the security schema handlers.
            - session (Session): The session object.
            - title: (str): A string with the question title.
            - body (str): A string with the question body.
            - option1 (str): A string with option1.
            - option2 (str): A string with option2.
            - option3 (str): A string with option3.
            - correct_answer (int): A integer for the correct option on question.
            - punctuation (float): A float with the punctuation of the question.
            - penalty (float): A float with the penalty of fail the question. 

        Raises:
            - ValueError: If any field is empty.
            - QuestionExistsError: If a question with the same title already exists.

        Returns:
            - Question: The created `Question` result.
        """

        '''response: ResponseData = auth_service.get_user_has_role(session.get('token'), 
                                                token_info['user_token']['user'], "Teacher")
        if response.is_successful() == False:
            raise ForbiddenOperationError'''
        try:
            new_question: Question = Questions.create(session, title, body, option1, 
                                    option2, option3, correct_answer, punctuation, penalty)
        except Exception as ex:
            raise ex
        return new_question

    @staticmethod
    def list_all(session: Session) -> List[Question]:
        """Lists every question.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Question]: A list of `Question` registers.
        """
        return Questions.list_all(session)

    @staticmethod
    def get_question_by_id(session: Session, id: int,) -> Optional[Question]:
        """ Determines whether a question exists or not.

        Args:
            - session (Session): The session object.
            - id (int): A integer for the id question.


        Returns:
            - Optional[Question]: The requested `Question` result.
        """
        try:
            question = Questions.get_question_by_id(session, id)
        except Exception as ex:
            raise ex
        return question

    @staticmethod
    def edit(auth_service: AuthService, token_info: Dict, session: Session, id: int, title: str,  body: str, option1: str, option2: str,
             option3: str, correct_answer: int, punctuation: float, penalty: float) -> Question:
        """ Edit an exist question.

        Args:
            - auth_service (AuthService): the authentication service
            - token_info (Dict): A dictionary of information provided by the security schema handlers.
            - session (Session): The session object.
            - id (int): A question id.
            - title: (str): A string with the question title.
            - body (str): A string with the question body.
            - option1 (str): A string with option1.
            - option2 (str): A string with option2.
            - option3 (str): A string with option3.
            - correct_answer (int): A integer for the correct option on question.
            - punctuation (float): A float with the punctuation of the question.
            - penalty (float): A float with the penalty of fail the question.
        Returns:
            - Optional[Question]: The edited `Question` result.
        """

        response: ResponseData = auth_service.get_user_has_role(session.get('token'), 
                                                token_info['user_token']['user'], "Teacher")
        if response.is_successful() == False:
            raise ForbiddenOperationError
        try:
            question = Questions.edit(session, id, title, body, option1, option2, option3, correct_answer, punctuation, penalty)
        except Exception as ex:
            raise ex
        return question


    @staticmethod
    def list_pending_for_user(session: Session, user: str) -> List[Question]:
        """Lists the pending questions for a user.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.

        Returns:
            - List[Question]: A list of questions.
        """
        try:
            questions = Questions.list_all(session)
            pending = []
            for question in questions:
                if Answers.get_answer(session, user, question.id) is None:     # type: ignore
                    pending.append(question)
        except Exception as ex:
            raise ex
        return pending

    @staticmethod
    def list_answered_for_user(session: Session, user: str) -> List[Question]:
        """Lists the answered questions for a user.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.

        Returns:
            - List[Question]: A list of questions.
        """
        try:
            questions = Questions.list_all(session)
            answered = []
            for question in questions:
                if Answers.get_answer(session, user, question.id) is not None:     # type: ignore
                    answered.append(question)
        except Exception as ex:
            raise ex
        return answered

