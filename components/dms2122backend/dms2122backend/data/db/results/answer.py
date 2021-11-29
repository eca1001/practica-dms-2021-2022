""" Answer Class Module
"""

from typing import Dict
from sqlalchemy import Table, MetaData, ForeignKey, Column, String, Integer  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2122backend.data.db.results.resultbase import ResultBase
class Answer(ResultBase):
    """ Definition and storage of answer ORM records.
    """

    def __init__(self, user: str, number: int, title: str):
        """ Constructor method.

        Initializes an answer record.

        Args:
            User: A string with students' name
            Number: Student questions' answer
            Tile: Questions' title
        """
        self.user : str = user
        self.number : int = number
        self.title : str = title

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
            'answers',
            metadata,
            Column('user', String(32), ForeignKey('user.username'), primary_key=True),
            Column('number', Integer, nullable=False),
            Column('id', Integer, ForeignKey('questions.id'), primaryKey=True)
        )