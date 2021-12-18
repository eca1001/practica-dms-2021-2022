""" Questions class module.
"""

import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.exc import QuestionExistsError
from dms2122backend.data.db.exc.questionorusernotfounderror import QuestionOrUserNotFoundError


class Questions():
    """ Class responsible of table-level questions operations.
    """
    @staticmethod
    def create(session: Session, title: str,  body: str, option1: str, option2: str, 
            option3: str, correct_answer: int, punctuation: float, penalty: float) -> Question:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
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
        if not title or not body or not option1 or not option2 or not option3 or not correct_answer or not punctuation or not penalty:
            raise ValueError('All fields are required.')
        try:
            new_question = Question(title, body, option1, option2, option3, correct_answer, punctuation, penalty)
            session.add(new_question)
            session.commit()
            return new_question
        except IntegrityError as ex:
            raise QuestionExistsError(
                'A question with title ' + title + ' already exists.'
                ) from ex
        
    @staticmethod
    def list_all(session: Session) -> List[Question]:
        """Lists every question.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Question]: A list of `Question` registers.
        """
        query = session.query(Question)
        return query.all()

    @staticmethod
    def get_question_by_id(session: Session, id: int,) -> Optional[Question]:
        """ Obtains a question given an id.

        Args:
            - session (Session): The session object.
            - id (int): A integer for the id question.

        Returns:
            - Optional[Question]: The created `Question` result.
        """
        if not id:
            raise ValueError('All fields are required.')
        try:
            query = session.query(Question).filter_by(id=id)
            question: Question = query.one()
        except NoResultFound:
            return None
        return question

    @staticmethod
    def edit(session: Session, id: int, title: str,  body: str, option1: str, option2: str, 
                option3: str, correct_answer: int, punctuation: float, penalty: float) -> Question:
        """ Edit an exist question.

        Args:
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
        if not title or not body or not option1 or not option2 or not option3 or not correct_answer or not punctuation or not penalty:
            raise ValueError('All fields are required.')
            
        edit_question = Questions.get_question_by_id(session, id)

        if edit_question is not None:
            edit_question.title = title
            edit_question.body = body
            edit_question.option1 = option1
            edit_question.option2 = option2
            edit_question.option3 = option3
            edit_question.correct_answer = correct_answer
            edit_question.punctuation = punctuation
            edit_question.penalty = penalty

            session.commit()

            return edit_question
        
        raise QuestionOrUserNotFoundError()

