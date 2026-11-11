'''
logger implementation
'''
from pathlib import Path
from logging.handlers import RotatingFileHandler
import logging
import sys


audit_logger = logging.getLogger("ETLAuditLogger")
audit_logger.setLevel(logging.INFO)
audit_logger.propagate = False 

handler = RotatingFileHandler(
    filename=f'{Path(__file__).resolve().parent.parent.parent}/logs/etl_audit.log', 
    maxBytes=5 * 1024 * 1024, # 5 MB
    backupCount=5, 
    encoding="utf-8"
)

formatter = logging.Formatter('[%(timestamp)s] [%(level)s] [Parent: %(parent_session_id)s] [Session: %(session_id)s] [%(task_name)s -> %(step_name)s]: %(message)s')
handler.setFormatter(formatter)
audit_logger.addHandler(handler)
