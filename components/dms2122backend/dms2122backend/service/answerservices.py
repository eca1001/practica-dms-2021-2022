""" AnswerServices class module.
"""
from typing import List, Dict
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema 
from dms2122backend.data.db.results import Answer
from dms2122backend.logic.answerlogic import AnswerLogic
from dms2122backend.data.rest import AuthService

class AnswersServices():
    """ Monostate class that provides high-level services to handle answer-related use cases.
    """

    @staticmethod
    def answer(auth_service: AuthService, username: str, number: int, questionId: int, schema: Schema, token_info: Dict) -> Dict:
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
        out: Dict = {}
        try:
            answer = AnswerLogic.create(auth_service, session, username, number, questionId, token_info)
            if answer is not None:
                out['id'] = answer.id
                out['username'] = answer.user
                out['number'] = answer.number

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def list_all_for_user(username: str, schema: Schema) -> List[Dict]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - username (str): The user name string.

        Returns:
            - List[Dict]: A list of dictionaries with the answers' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        try:
            answers: List[Answer] = AnswerLogic.list_all_for_user(session, username)
            for answer in answers:
                out.append({
                    'id': answer.id,
                    'username': answer.user,
                    'number': answer.number
                })
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out



    @staticmethod
    def list_all_for_question(questionId: int, schema: Schema) -> List[Dict]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - questionId (int): Id of the question.

        Returns:
            - List[Dict]: A list of dictionaries with the answers' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        try:
            answers: List[Answer] = AnswerLogic.list_all_for_question(session, questionId)
            for answer in answers:
                out.append({
                    'id': answer.id,
                    'username': answer.user,
                    'number': answer.number
                })
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out


    @staticmethod
    def question_has_answers(auth_service: AuthService, token_info: Dict,questionId: int, schema: Schema) -> bool:
        """Return True or False if a certain question has answers.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - questionId (int): Id of the question.

        Returns:
            - bool: True if question has answers, False if not
        """
        session: Session = schema.new_session()
        try:
            answer: bool = AnswerLogic.question_has_answers(auth_service,token_info,session, questionId)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return answer

    @staticmethod
    def get_answer(user: str, id: int, schema: Schema) -> Dict:
        """Return a answer of a certain question and user.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - user (str): The user name string.
            - id (int): The question id.

        Returns:
            - Dict: Answer of the question.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            answer: Answer = AnswerLogic.get_answer(session, user, id)
            if answer is not None:
                out['id'] = answer.id
                out['username'] = answer.user
                out['number'] = answer.number
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out


    @staticmethod
    def answer_punctuation(answer:Answer,schema: Schema)->float:
        session: Session = schema.new_session()   
        punctuation: float=0     
        try:
            punctuation = AnswerLogic.answer_punctuation(session,answer)
            schema.remove_session()
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return punctuation