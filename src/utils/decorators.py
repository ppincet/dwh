import functools
from utils.constants.log_levels import SUCCESS, EXCEPTION, FINEST
from utils.common import session_container, create_session, commit_session

def process_task(task_name : str = 'ETL PROC', lg_level: str = FINEST):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = create_session(task_name, )
            token = session_container.set(session)
            try:
                result = func(*args, **kwargs)
                session["status"] = SUCCESS
                return result
            except Exception as e:
                session["status"] = EXCEPTION
                raise
            finally:
                commit_session(lg_level)
                session_container.reset(token)
        return wrapper
    return decorator