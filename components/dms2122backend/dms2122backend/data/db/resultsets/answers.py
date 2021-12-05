""" Answers class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.exc.questionorusernotfounderror import QuestionOrUserNotFoundError
from dms2122backend.data.db.exc import UserNotFoundError

class Answers():
    """ Class responsible of table-level answers operations.
    """
    @staticmethod
    def answer(session: Session, username: str, number: int, questionId: int) -> Answer:
        """ Answers a question.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - 

        Raises:  
            - ValueError: If any field is empty.
            - UserNotFoundError: If the user who answers the question does not exist.
            - QuestionNotFoundError: If the question to be answered does not exist.

        Returns:
            - Answer: The created `Answer` result.
        """
        if not username or not questionId or not number:
            raise ValueError('All fields are required.')
        try:
            new_answer = Answer(username, number, questionId)
            session.add(new_answer)
            session.commit()
            return new_answer
        except IntegrityError as ex:
            session.rollback()
            raise QuestionOrUserNotFoundError() from ex
        except:
            session.rollback()
            raise
        
    @staticmethod
    def list_all_for_user(session: Session, user: str) -> List[Answer]:
        """Lists the `answers made by a certain user.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.

        Raises:
            - ValueError: If the username is missing.

        Returns:
            - List[Answer]: A list of answer registers with the user answers.
        """
        if not user:
            raise ValueError('A username is required.')
        query = session.query(Answer).filter_by(
            user=user
        )
        return query.all()

    @staticmethod
    def list_all_for_question(session: Session, id: int) -> List[Answer]:
        """Lists the `answers made to a certain question.

        Args:
            - session (Session): The session object.
            - id (int): The question id.

        Raises:
            - ValueError: If the question id is missing.

        Returns:
            - List[Answer]: A list of answer registers with the question answers.
        """
        if not id:
            raise ValueError('A question id is required.')
        query = session.query(Answer).filter_by(
            id=id
        )
        return query.all()

    @staticmethod
    def question_has_answers(session: Session, id: int) -> bool:
        """Finds out if a certain question has been answered.

        Args:
            - session (Session): The session object.
            - id (int): The question id.

        Raises:
            - ValueError: If the question id is missing.

        Returns:
            - bool: a boolean that indicates whether a question has answers.
        """
        if not id:
            raise ValueError('A question id is required.')
        questions = Answers.list_all_for_question(session, id)

        return len(questions) != 0

    @staticmethod
    def get_answer(session: Session, user: str, id: int) -> Answer:
        """Return a answer of a certain question and user.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.
            - id (int): The question id.

        Raises:
            - ValueError: If the username is missing.

        Returns:
            - Answer: Answer of the question.
        """
        if not user:
            raise ValueError('A username is required.')
        query = session.query(Answer).filter_by(
            user=user, id=id
        )
        return query.one_or_none()