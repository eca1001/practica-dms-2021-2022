""" Answers class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.exc import QuestionNotFoundError
from dms2122backend.data.db.exc import UserNotFoundError

class Questions():
    """ Class responsible of table-level answers operations.
    """
    @staticmethod
    def answer(session: Session) -> Answer:
        """ Answers a question.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - 

        Raises:
            - ValueError: If either the title or the [AAAAAAAAAAAAAAAAAAAAAAA COMPLETAAAAAAAAAAAAAAAAR] is empty.
            - UserNotFoundError: If the user who answers the question does not exist.
            - QuestionNotFoundError: If the question to be answered does not exist.

        Returns:
            - Answer: The created `Answer` result.
        """