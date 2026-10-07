import datetime
from utils import db_helper, common
from utils.constants.log_levels import FINEST, INFO, SUCCESS, WARNING, EXCEPTION
from utils.constants.log_levels import MODE_FULL, MODE_MEDIUM, MODE_SUCCESS
from config.settings import RETRY_DELAY, MAX_RETRIES
from typing import List, Dict, Optional
import importlib
from utils.common import session_container
from utils.decorators import process_task, retry_srv
import json
# from config.settings import MAX_RETRIES, 

@process_task('create_refs', FINEST)
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

# def get_fact_table(period: str = 'AUTO', is_odinass = True) -> None:
#     session = session_container.get()
#     period_range = (
#         common.get_rolling_window_standard(True) if period == 'AUTO' else common.parse_date_range(period, is_odinass)
#     )
#     for attempt in range(1, MAX_RETRIES + 1):
#         try:
#             common.add_log(session, 'start etl', f'get odinass fact (attempt {attempt}/({MAX_RETRIES})')
#             db_helper.get_fact_table(*period_range)
#             common.add_log(session, 'start etl', 'get oodinass fact - finished')
#         except:
@retry_srv(MAX_RETRIES, RETRY_DELAY)
@process_task('LSF FT', FINEST)
def upload_lsf_ft(period_from: str, period_to: str):
    db_helper.upload_ft(period_from, period_to)
def check_updates() -> None:
    print('check done')
@process_task('ETL PROC', FINEST)
def start_etl() -> None:
    session = session_container.get()
    print(datetime.datetime.now())
    # try:
    common.add_log(session, 'start etl', 'enter etl')
    # result = upload_docs()
    # result = get_fact_table()
    upload_lsf_ft('2026-10-01 00:00:00', '2026-10-02 00:00:00')
    #result = check_updates()
    # commit log
    common.add_log(session, 'done etl', 'done etl', SUCCESS)
    print(datetime.datetime.now())
    # except Exception as e:
    #     common.add_log(session, 'start etl', 'etl failed', EXCEPTION)
    #     print(f'exception in start etl: {e}')
def do_init(content: dict[str, str], aliases_only: bool) -> None:
    session = session_container.get()
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
@process_task(FINEST)
def create_lsf_ref(content: Dict[str, Optional[str]]) -> None:
    session = session_container.get()
    for k, v in content.items():
        print(k)
        db_helper.upload_lsf_ref(k)
    
    

