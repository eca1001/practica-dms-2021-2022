""" StatsLogic class module.
"""
from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.logic.answerlogic import AnswerLogic
from dms2122backend.logic.questionlogic import QuestionLogic
from dms2122backend.data.db.results import Answer, Question

class StatsLogic():
    """ Monostate class that provides logic-level operations to handle statistics-related use cases.
    """

    @staticmethod
    def all_questions_puntuation(session: Session)->float:
        questions:List[Question]=QuestionLogic.list_all(session)
        total_punctuation:float=0
        for ques in questions:
            total_punctuation=total_punctuation+ques.punctuation
        return total_punctuation

    @staticmethod
    def user_stats(session: Session, user: str)-> Dict:
        values: Dict = {}
        try:
            user_answers:List[Answer]=AnswerLogic.list_all_for_user(session,user)

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
        
        