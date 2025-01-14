""" StatsLogic class module.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.logic.answerlogic import AnswerLogic
from dms2122backend.logic.questionlogic import QuestionLogic
from dms2122backend.data.db.results import Answer, Question
from dms2122backend.data.db.resultsets import Answers

class StatsLogic():
    """ Monostate class that provides logic-level operations to handle statistics-related use cases.
    """

    @staticmethod
    def all_questions_puntuation(session: Session)->float:
        questions:List[List]=QuestionLogic.list_all(session)
        total_punctuation:float=0
        for ques in questions:
            question: Question = ques[0]
            total_punctuation=total_punctuation+question.punctuation
        return total_punctuation

    @staticmethod
    def user_stats(session: Session, user: str)-> Dict:
        values: Dict = {}
        try:
            user_answers:List[Answer]=Answers.list_all_for_user(session, user)

            n_answers: int = len(user_answers)
            user_punctuation:float = 0
            answered_questions_punctuation:float=0
            score_answered:float=0
            score_all_questions:float=0
            punt: Optional[float] = 0
            for ans in user_answers:
                question: Optional[Question] = QuestionLogic.get_question_by_id(session,ans.id)
                if question is not None:
                    punt = AnswerLogic.answer_punctuation(session,ans)
                    if punt is not None:
                        user_punctuation=user_punctuation+punt
                    answered_questions_punctuation=answered_questions_punctuation+question.punctuation
            
            score_answered=user_punctuation/answered_questions_punctuation*10
            score_all_questions=user_punctuation/StatsLogic.all_questions_puntuation(session)*10
            values['n_answers']=n_answers
            values['user_punctuation']=user_punctuation
            values['score_answered']=score_answered
            values['score_all_questions']=score_all_questions

            return values
        except Exception as ex:
            raise ex

    @staticmethod
    def questions_stats(session: Session)-> List[Dict]:
        try:
            questions:List[List]=QuestionLogic.list_all(session)
            values: List = []
            for ques in questions:
                question: Question = ques[0]
                answers: List[Answer] = AnswerLogic.list_all_for_question(session,question.id) # type: ignore
                n_answers=len(answers)
                dic: Dict={}
                if n_answers >0:
                    n_opcion1:int=0
                    n_opcion2:int=0
                    n_opcion3:int=0
                    punt: Optional[float] = 0
                    question_punctuation:float = 0                    
                    avg_punctuation:float=0
                    for ans in answers:
                        opcion:int=ans.number
                        if opcion==1:
                            n_opcion1=n_opcion1+1
                        elif opcion==2:
                            n_opcion2=n_opcion2+1
                        else:
                            n_opcion3=n_opcion3+1
                        punt = AnswerLogic.answer_punctuation(session,ans)
                        if punt is not None:
                            question_punctuation=question_punctuation+punt
                    dic['title']=question.title
                    dic['n_answers']=n_answers
                    dic['n_opcion1']=n_opcion1
                    dic['n_opcion2']=n_opcion2
                    dic['n_opcion3']=n_opcion3
                    dic['avg_punctuation']=question_punctuation/(n_answers)
                    values.append(dic)
                else:
                    dic['title']=question.title
                    dic['n_answers']=0
                    dic['n_opcion1']=0
                    dic['n_opcion2']=0
                    dic['n_opcion3']=0
                    dic['avg_punctuation']=0
                    values.append(dic)
            return values   
        except Exception as ex:
            raise ex
        
    @staticmethod
    def users_stats(session: Session) -> List[Dict]:
        try:
            values: List = []
            answers:List[Answer]=AnswerLogic.list_all(session)
            all_users:List=[]
            for answer in answers:
                user:str=answer.user
                if not user in all_users:
                    all_users.append(user)
            
            for user in all_users:
                dic:Dict=StatsLogic.user_stats(session,user)
                dic['username']=user
                values.append(dic)

            return values
        except Exception as ex:
            raise ex



