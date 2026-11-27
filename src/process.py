import datetime
from utils import db_helper, common
from utils.constants.log_levels import FINEST, INFO, SUCCESS, WARNING, EXCEPTION
from utils.constants.log_levels import MODE_FULL, MODE_MEDIUM, MODE_SUCCESS
from config.settings import RETRY_DELAY, MAX_RETRIES
from typing import List, Dict, Optional
import importlib
from utils.common import session_container, get_rolling_window,to_opt_str
from utils.decorators import process_task, retry_srv, persist_audit_trail
import json

@persist_audit_trail
@process_task('global')
def perform_global():
    try:
        session = session_container.get()
        common.add_log(session, 'global','start', INFO)
        print('before bu')
        db_helper.backup_subkonto()
        # content = common.get_refs('B:C') # odinass
        # create_refs(content, False, False, session)
        # todo lsf region
        common.add_log(session, 'global', 'finish', INFO)
    except Exception as e:
        print(f'from global: {e}')
        common.add_log(session, 'global', e, EXCEPTION)
        
@process_task('create_refs')
def create_refs(content: Dict[str, Optional[str]], aliases_only: bool, view_only: bool, session) -> None:
    try:
        common.add_log(session, 'refs/views creation', 'start common', INFO)
        for k, v in content.items():
            if k is None: continue
            if not view_only:
                print(f'{k}({v}) start')
                db_helper.create_ref(f'{k}', 
                    v if v is not None else f'VREF{k}',
                    aliases_only,
                    session)
                status = f'{k}({v}) done'
                print(f'{datetime.datetime.now()}:{status}')
                common.add_log(session, 'create refs', status)
            else:
                db_helper.create_view_standalone(k, v, aliases_only, session)
            common.add_log(session, 'refs/views creation', status, SUCCESS)
    except Exception as e:
        common.add_log(session, 'refs/views creation', e, EXCEPTION)
        raise

def check_etl_bot():
    db_helper.check_etl_bot()

# @retry_srv(MAX_RETRIES, RETRY_DELAY)
@process_task('ODINASS PROC')
def get_fact_table(period: str = 'AUTO', is_odinass = True) -> None:
    period_range = (
        common.get_rolling_window_standard(True) if period == 'AUTO' else common.parse_date_range(period, is_odinass)
    )
    print(*period_range)
    db_helper.get_fact_table(*period_range)

@retry_srv(MAX_RETRIES, RETRY_DELAY)
@process_task('LSF FT PROC - GROUP')
def prepare_group():
    db_helper.prepare_group()
@retry_srv(MAX_RETRIES, RETRY_DELAY)
@process_task('LSF FT PROC - GROUP')
def group_lsf(period_from, period_to):
    db_helper.group(period_from, period_to)

@retry_srv(MAX_RETRIES, RETRY_DELAY)
@process_task('LSF FT PROC - PREPARE')
def prepare_upload():
    db_helper.prepare_upload()
@retry_srv(MAX_RETRIES, RETRY_DELAY)
@process_task('LSF FT PROC')
def upload_lsf_ft(period_from: str, period_to: str):
    db_helper.upload_ft(period_from, period_to, 0)
    db_helper.upload_ft(period_from, period_to, 1)
@persist_audit_trail
@process_task('ETL PROC')
def start_etl(lg_lvl) -> None:
    session = session_container.get()
    try:
        common.add_log(session, 'start etl', 'enter etl')
        # result = upload_docs()
        # result = get_fact_table()
        prepare_upload()
        # upload_lsf_ft('2026-10-01 00:00:00', '2026-10-31 00:00:00')
        prepare_group()
        group_lsf('2026-10-01', '2026-10-31')
        #result = check_updates()
        common.add_log(session, 'done etl', 'done etl', SUCCESS)
    except Exception as e:
        common.add_log(session, 'start etl', 'etl failed', EXCEPTION)
        raise
@process_task('ETL PROC')
def do_init(content: dict[str, str], aliases_only: bool) -> None:
    session = session_container.get()
    pass
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
@process_task()
def create_lsf_ref(content: Dict[str, Optional[str]]) -> None:
    session = session_container.get()
    for k, v in content.items():
        print(k)
        db_helper.upload_lsf_ref(k)
    
    

