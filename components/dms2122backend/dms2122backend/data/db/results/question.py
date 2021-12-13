""" Question Class Module
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String, Integer, Float  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2122backend.data.db.results.resultbase import ResultBase
from dms2122backend.data.db.results.answer import Answer

class Question(ResultBase):
    """ Definition and storage of question ORM records.
    """

    def __init__(self, title: str,  body: str, option1: str, option2: str, option3: str, correct_answer: int, punctuation: float, penalty: float):
        """ Constructor method.

        Initializes a question record.

        Args:
            - title: (str): A string with the question title.
            - body (str): A string with the question body.
            - option1 (str): A string with option1.
            - option2 (str): A string with option2.
            - option3 (str): A string with option3.
            - correct_answer (int): A integer for the correct option on question.
            - punctuation (float): A float with the punctuation of the question.
            - penalty (float): A float with the penalty of fail the question.
        """
        self.title: str = title
        self.body: str = body
        self.option1: str = option1
        self.option2: str = option2
        self.option3: str = option3
        self.correct_answer: int = correct_answer
        self.punctuation: float = punctuation
        self.penalty: float = penalty

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.

        Args:
            - metadata (MetaData): The database schema metadata
                        (used to gather the entities' definitions and mapping)

        Returns:
            - Table: A `Table` object with the table definition.
        """

        return Table(
            'questions',
            metadata,
            Column('id', Integer, autoincrement= 'auto', primary_key=True),
            Column('title', String(64), nullable=False),
            Column('body', String(256), nullable=False),
            Column('option1', String(256), nullable=False),
            Column('option2', String(256), nullable=False),
            Column('option3', String(256), nullable=False),
            Column('correct_answer', Integer, nullable=False),
            Column('punctuation', Float(2,2), nullable=False),
            Column('penalty', Float(2,2), nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.

        Returns:
            - Dict: A dictionary with the mapping properties.
        """
        return {
            'questions': relationship(Answer, backref='question')
        }

         