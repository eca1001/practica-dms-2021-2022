""" StatsServices class module.
"""
from dms2122backend.data.db import Schema 
from sqlalchemy.orm.session import Session  # type: ignore
from typing import List, Dict, Optional
from dms2122backend.logic.statslogic import StatsLogic

class StatsServices():
    """ Monostate class that provides high-level services to handle stats-related use cases.
    """

    @staticmethod
    def user_stats(username: str, schema: Schema)-> Dict:
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            out = StatsLogic.user_stats(session, username)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def questions_stats(schema: Schema) -> List[Dict]:
        session: Session = schema.new_session()
        out: List[Dict] = []
        try:
            out = StatsLogic.questions_stats(session)
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out      