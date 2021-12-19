""" REST API controllers responsible of handling the stats operations.
"""
from flask import current_app, session
from dms2122backend.service import StatsServices
from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus

def user_stats(user: str)->Tuple[Union[List, str], Optional[int]]:
    """Get a user stats.

    Args:
        - user (str): A user whose statistics we want to know.

    Returns:
        - Tuple[Union[List, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
    """
    with current_app.app_context():
        try:
            user_stats: List = StatsServices.user_stats(
                user, current_app.db
            )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (user_stats, HTTPStatus.OK.value)