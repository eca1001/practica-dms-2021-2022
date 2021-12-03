""" AnswerServices class module.
"""
from typing import List, Dict
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema 
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.resultsets import Answers

class AnswersServices():
    """ Monostate class that provides high-level services to handle answer-related use cases.
    """

    @staticmethod
    def answer(username: str, number: int, questionId: int, schema: Schema) -> None:
        """Answer a question.

        Args:
            - schema (Schema): A database handler where the users are mapped into.            

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new user's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            Answers.answer(session, username, number, questionId)

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()

    @staticmethod
    def list_all_for_user(schema: Schema, username: str) -> List[Answer]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        session: Session = schema.new_session()
        answer = Answers.list_all_for_user(session, username)
        schema.remove_session()
        return answer


    @staticmethod
    def list_all_for_question(schema: Schema, questionId: int) -> List[Answer]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        session: Session = schema.new_session()
        answer = Answers.list_all_for_question(session, questionId)
        schema.remove_session()
        return answer

    @staticmethod
    def question_has_answers(schema: Schema, questionId: int) -> bool:

        session: Session = schema.new_session()
        answer = Answers.question_has_answers(session, questionId)
        schema.remove_session()
        return answer