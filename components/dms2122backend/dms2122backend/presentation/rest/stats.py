""" REST API controllers responsible of handling the stats operations.
"""
from flask import current_app, session
from dms2122backend.service.statsservices import StatsServices
from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus

def user_stats(username: str)->Tuple[Union[Dict, str], Optional[int]]:
    """Get a user stats.

    Args:
        - username (str): A user whose statistics we want to know.

    Returns:
        - Tuple[Union[List, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
    """
    with current_app.app_context():
        try:
            user_stats: Dict = StatsServices.user_stats( username, current_app.db )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (user_stats, HTTPStatus.OK.value)

def questions_stats() -> Tuple[Union[List[Dict], str], Optional[int]]:
    with current_app.app_context():
        try:
            questions_sta: List[Dict]  = StatsServices.questions_stats(current_app.db )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (questions_sta, HTTPStatus.OK.value)

def users_stats() -> Tuple[Union[List[Dict], str], Optional[int]]:
    with current_app.app_context():
        try:
            users_stats: List[Dict]  = StatsServices.users_stats(current_app.db )
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)        
    return (users_stats, HTTPStatus.OK.value)