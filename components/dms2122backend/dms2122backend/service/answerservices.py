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
            - username (str): The user name string.
            - number (int): Answer's selection number by the student.
            - questionId (int): Id of the question.
            - schema (Schema): A database handler where the users are mapped into.

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new user's data.
        """

        session: Session = schema.new_session()
        try:
            Answers.answer(session, username, number, questionId)

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()

    @staticmethod
    def list_all_for_user(username: str, schema: Schema) -> List[Answer]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - username (str): The user name string.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        session: Session = schema.new_session()
        answer = Answers.list_all_for_user(session, username)
        schema.remove_session()
        return answer


    @staticmethod
    def list_all_for_question(questionId: int, schema: Schema) -> List[Answer]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - questionId (int): Id of the question.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        session: Session = schema.new_session()
        answer = Answers.list_all_for_question(session, questionId)
        schema.remove_session()
        return answer


    @staticmethod
    def question_has_answers(questionId: int, schema: Schema) -> bool:
        """Return True or False if a certain question has answers.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - questionId (int): Id of the question.

        Returns:
            - nool: True if question has answers, False if not
        """
        session: Session = schema.new_session()
        answer = Answers.question_has_answers(session, questionId)
        schema.remove_session()
        return answer

    @staticmethod
    def get_answer(user: str, id: int, schema: Schema) -> Answer:
        """Return a answer of a certain question and user.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - user (str): The user name string.
            - id (int): The question id.

        Returns:
            - Answer: Answer of the question.
        """
        session: Session = schema.new_session()
        answer = Answers.get_answer(session, user, id)
        schema.remove_session()
        return answer