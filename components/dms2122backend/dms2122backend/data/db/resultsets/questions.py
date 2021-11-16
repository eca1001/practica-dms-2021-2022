""" Questions class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.exc import QuestionExistsError


class Questions():
    """ Class responsible of table-level questions operations.
    """
    @staticmethod
    def create(session: Session) -> Question:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - 

        Raises:
            - ValueError: If either the title or the [AAAAAAAAAAAAAAAAAAAAAAA COMPLETAAAAAAAAAAAAAAAAR] is empty.
            - QuestionExistsError: If a question with the same title already exists.

        Returns:
            - Question: The created `Question` result.
        """