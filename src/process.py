import datetime
from utils import db_helper, common
from utils.constants.log_levels import FINEST, INFO, SUCCESS, WARNING, EXCEPTION
from utils.constants.log_levels import MODE_FULL, MODE_MEDIUM, MODE_SUCCES 
from typing import List, Dict, Optional
import importlib
import contextvars
import functools

#region session decorator
session_container = contextvars.ContextVar('session_container', default=None)

def process_task(task_name: str, lg_level: str ):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = common.create_session()
            token = session_container.set(session)
            try:
                result = func(*args, **kwargs)
                session["context"]["status"] = "SUCCESS"
                return result
            except Exception as e:
                session["context"]["status"] = "FAILED"
                raise
            finally:
                common.commit_session(session, lg_level=lg_level)
                session_container.reset(token)
        return wrapper
    return decorator

#endregion


def create_refs(content: Dict[str, Optional[str]], aliases_only: bool, view_only: bool) -> None:
    try:
        common.add_log(session, 'refs/views creation', 'start common', INFO)
        for k, v in content.items():
            if k is None: continue
            if not view_only:
                db_helper.create_ref(f'{k}', 
                    v if v is not None else f'VREF{k}',
                    aliases_only,
                    session)
            else:
                db_helper.create_view_standalone(k, v, aliases_only, session)
            common.add_log(session, 'refs/views creation', f'{k} done', SUCCESS)
    except Exception as e:
        common.add_log(session, 'refs/views creation', '', EXCEPTION)
    finally: 
        # filter & commit session
        print(f'{datetime.datetime.now()} : done create refs')

def check_etl_bot():
    db_helper.check_etl_bot()

def get_fact_table(period: str = 'AUTO', is_odinass = True) -> None:
    period_range = (
        common.get_rolling_window_standard(True) if period == 'AUTO' else common.parse_date_range(period, is_odinass)
    )
    db_helper.get_fact_table(*period_range, session)
def check_updates() -> None:
    print('check done')
def start_etl() -> None:
    try:
        print('start etl')
        session['command'] = 'START ETL'
        result = upload_docs()
        #result = get_fact_table()
        #result = check_updates()
        # commit log
    except Exception as e:
        # common.add_log(session, 'START ETL', , )
        print(f'exception : {e}')
def do_init(content: dict[str, str], aliases_only: bool) -> None:
    create_refs(content, aliases_only, False, session)
def perform_command(module_name: str, command: str, args: dict[str, str]) -> None:
    method = getattr(importlib.import_module(module_name), command, **args)
    if callable(method): method(**args)
def upload_docs() -> None:
    """uploads all documents. uses get_rolling_window_standard.
    
        Args:
            None.
        Returns:
            None.
    """
    db_helper.upload_docs(*common.get_rolling_window_standard(True))
    
    

