import functools
import time
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
def retry_srv(retries: int = 3, delay: float = 2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == retries: raise
                    
                    print(f"⚠️ [Retry] {attempt} for {retries}  ('{func.__name__}') :  {e}.")
                    time.sleep(delay)
            raise last_exception
        return wrapper

