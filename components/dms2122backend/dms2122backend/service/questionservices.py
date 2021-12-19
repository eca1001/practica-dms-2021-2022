""" QuestionServices class module.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.rest import AuthService
from dms2122backend.data.db import Schema 
from dms2122backend.data.db.results import Question
from dms2122backend.logic import QuestionLogic

class QuestionsServices():
    """ Monostate class that provides high-level services to handle question-related use cases.
    """

    @staticmethod
    def get_question_by_id(id: int, schema: Schema)-> Dict:
        """

        Args:
            - schema (Schema): A database handler where the users are mapped into.
            - id (int): A question id.
            
        Returns:
            - Dict: A dictionary with the requested question's data.
        """        
        
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            question = QuestionLogic.get_question_by_id(session, id)
            if question is not None:
                out['id'] = question.id     # type: ignore
                out['title'] = question.title
                out['body'] = question.body
                out['option1'] = question.option1
                out['option2'] = question.option2
                out['option3'] = question.option3
                out['correct_answer'] = question.correct_answer
                out['punctuation'] = question.punctuation
                out['penalty'] = question.penalty
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

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
        questions: List[Question] = QuestionLogic.list_all(session)
        for question in questions:
            out.append({
                'id': question.id,     # type: ignore
                'title': question.title,
                'body': question.body,
                'option1': question.option1,
                'option2': question.option2,
                'option3': question.option3,
                'correct_answer': question.correct_answer,
                'punctuation': question.punctuation,
                'penalty': question.penalty
            })
        schema.remove_session()
        return out

    @staticmethod
    def create_question(auth_service: AuthService, token_info: Dict, title: str,  body: str, option1: str, option2: str, option3: str, 
                correct_answer: int, punctuation: float, penalty: float, schema: Schema) -> Dict:
        """Creates a question.

        Args:
            - auth_service (AuthService): allows to verify users roles.
            - token_info (Dict): A dictionary of information provided by the security schema handlers.
            - title: (str): A string with the question title.
            - body (str): A string with the question body.
            - option1 (str): A string with option1.
            - option2 (str): A string with option2.
            - option3 (str): A string with option3.
            - correct_answer (int): A integer for the correct option on question.
            - punctuation (float): A float with the punctuation of the question.
            - penalty (float): A float with the penalty of fail the question.
            - schema (Schema): A database handler where the users are mapped into.            

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new question's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_question: Question = QuestionLogic.create(auth_service, token_info, session, title, body, option1, 
                                        option2, option3, correct_answer, punctuation, penalty)
            out['id'] = new_question.id     # type: ignore
            out['title'] = new_question.title
            out['body'] = new_question.body
            out['option1'] = new_question.option1
            out['option2'] = new_question.option2
            out['option3'] = new_question.option3
            out['correct_answer'] = new_question.correct_answer
            out['punctuation'] = new_question.punctuation
            out['penalty'] = new_question.penalty
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def edit_question(auth_service: AuthService, token_info: Dict, id: int, title: str,  body: str, option1: str, option2: str, option3: str,
                 correct_answer: int, punctuation: float, penalty: float, schema: Schema) -> Dict:
        """ Edit an exist question.

        Args:
            - auth_service (AuthService): allows to verify users roles.
            - token_info (Dict): A dictionary of information provided by the security schema handlers.
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
            - Dict: A dictionary with the edited question's data.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            question = QuestionLogic.edit(auth_service, token_info, session, id, title, body, option1, option2, 
                            option3, correct_answer, punctuation, penalty)
            out['id'] = question.id     # type: ignore
            out['title'] = question.title
            out['body'] = question.body
            out['option1'] = question.option1
            out['option2'] = question.option2
            out['option3'] = question.option3
            out['correct_answer'] = question.correct_answer
            out['punctuation'] = question.punctuation
            out['penalty'] = question.penalty
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out


    @staticmethod
    def list_pending_for_user(schema: Schema, user: str) -> List[Dict]:
        """Lists the pending questions for a user.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - user (str): The user name string.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        try:
            questions: List[Question] = QuestionLogic.list_pending_for_user(session, user)
            for question in questions:
                out.append({
                    'id': question.id,     # type: ignore
                    'title': question.title,
                    'body': question.body,
                    'option1': question.option1,
                    'option2': question.option2,
                    'option3': question.option3,
                    'correct_answer': question.correct_answer,
                    'punctuation': question.punctuation,
                    'penalty': question.penalty
                })
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def list_answered_for_user(schema: Schema, user: str) -> List[Dict]:
        """Lists the answered questions for a user.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - user (str): The user name string.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        try:
            questions: List[Question,float] = QuestionLogic.list_answered_for_user(session, user)
            for question in questions:
                out.append({ 'question':{
                    'id': question[0].id,     # type: ignore
                    'title': question[0].title,
                    'body': question[0].body,
                    'option1': question[0].option1,
                    'option2': question[0].option2,
                    'option3': question[0].option3,
                    'correct_answer': question[0].correct_answer,
                    'punctuation': question[0].punctuation,
                    'penalty': question[0].penalty},
                'punctuation': question[1]
                })
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
