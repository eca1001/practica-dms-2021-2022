""" QuestionServices class module.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema 
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.resultsets import Questions

class QuestionsServices():
    """ Monostate class that provides high-level services to handle question-related use cases.
    """

    @staticmethod
    def get_question(title: str,  body: str, option1: str, option2: str, option3: str, correct_answer: int, punctuation: float, penalty: float, schema: Schema)-> Optional[Question]:
        """

        Args:
            - schema (Schema): A database handler where the users are mapped into.
            
        Returns:
            -
        """        
        
        session: Session = schema.new_session()
        question = Questions.get_question(session, title, body, option1, option2, option3, correct_answer, punctuation, penalty)
        schema.remove_session()
        return question

    @staticmethod
    def get_question_by_id( id: int, schema: Schema)-> Optional[Question]:
        """

        Args:
            - schema (Schema): A database handler where the users are mapped into.
            
        Returns:
            -
        """        
        
        session: Session = schema.new_session()
        question = Questions.get_question_by_id(session, id)
        schema.remove_session()
        return question

    @staticmethod
    def list_questions(schema: Schema) -> List[Dict]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        questions: List[Question] = Questions.list_all(session)
        for question in questions:
            out.append({
                'title': question.title
            })
        schema.remove_session()
        return out

    @staticmethod
    def create_question(title: str,  body: str, option1: str, option2: str, option3: str, correct_answer: int, punctuation: float, penalty: float, schema: Schema) -> Dict:
        """Creates a question.

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
            new_question: Question = Questions.create(session, title, body, option1, option2, option3, correct_answer, punctuation, penalty)
            out['title'] = new_question.title
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def edit_question(id: int, title: str,  body: str, option1: str, option2: str, option3: str, correct_answer: int, punctuation: float, penalty: float, schema: Schema) -> Optional[Question]:
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
        session: Session = schema.new_session()
        try:
            question = Questions.edit(session, title, body, option1, option2, option3, correct_answer, punctuation, penalty)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return question
