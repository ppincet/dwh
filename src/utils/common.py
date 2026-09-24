import datetime
import pandas as pd
import uuid
from utils.constants.log_levels import SUCCESS, WARNING, EXCEPTION

def filter_logs(logs: list[dict], lg_level: str) -> list[dict]:
    """returns back filtered audit trail upon log level.
        Args:
            logs (list[dict]): audit trail.
            lg_level (str): audit level.
        Returns: 
            list[dict]: filtered audit trail

    """
    if lg_level == 'FULL':
        return logs    
    if lg_level == 'MEDIUM':
        allowed = {SUCCESS, WARNING, EXCEPTION}
        return [log for log in logs if log['level'] in allowed]
    
    if lg_level == 'SUCCESS':
        allowed = {SUCCESS, EXCEPTION}
        return [log for log in logs if log['level'] in allowed]
    return logs

def create_session(command: str = "DEFAULT") -> dict:
    """creates a session based on the provided command.

    Args:
        command (str, optional): command identifier for the session. defaults to "DEFAULT".

    Returns:
        dict: Created session object.
    """
    return {
        "session_id": str(uuid.uuid4()),
        "command": command,
        "status": "RUNNING",
        "start_time": datetime.datetime.now().isoformat(),
        "end_time": None,
        "metrics": {},
        "logs": []
    }

def add_log(session: dict, step_name: str, message: str, level: str = "INFO") -> None:
    """adds an audit trail entry.

        Args:
            session (dict): active session.
            step_name (str): process step name.
            message (str): message.
            level (str, optional): audit trail level. defaults to 'INFO'.
        Returns:
            None


    """
    session["logs"].append({
        "timestamp": datetime.datetime.now().isoformat(),
        "level": level,
        "step_name": step_name,
        "message": message
    })
def parse_date_range(date_str: str, odinass: bool = True) -> tuple[datetime.datetime, datetime.datetime]:
    date_str = date_str.strip()
    parts = [p.strip() for p in date_str.split('-')]
    
    if '-' not in date_str:
        start = datetime.datetime.strptime(date_str, '%Y%m%d')
        end = start.replace(hour=23, minute=59, second=59)
    else:
        left, right = parts[0], parts[1]
        
        if not left and right:
            start = datetime.datetime(2001 if odinass else 1753, 1, 1, 0, 0, 0)
            end = datetime.datetime.strptime(right, '%Y%m%d').replace(hour=23, minute=59, second=59)
        elif left and not right:
            start = datetime.datetime.strptime(left, '%Y%m%d')
            end = datetime.datetime.now().replace(hour=23, minute=59, second=59)
        else:
            start = datetime.datetime.strptime(left, '%Y%m%d')
            end = datetime.datetime.strptime(right, '%Y%m%d').replace(hour=23, minute=59, second=59)
    if odinass:
        if left or '-' not in date_str:
            start = start.replace(year=start.year + 2000)
        end = end.replace(year=end.year + 2000)
    return start, end

def get_next_id(max_bytes: bytes) -> bytes:
    if not max_bytes:
        current_int = 0
    else:
        current_int = int.from_bytes(max_bytes, byteorder='big')

    next_int = current_int + 1
    return next_int.to_bytes(16, byteorder='big')

def get_rolling_window_standard(is_odinass: bool) -> tuple[datetime.datetime, datetime.datetime]:
    """returns back a tuple with 1st day at midnight of prev month & current day at the end of day
        Args:
            is_odinass (bool): represents odinass year offset flag.
        Returns:
            tuple[datetime.datetime, datetime.datetime]: a tuple containing start_date and end_date.
    """
    today = datetime.date.today()
    first_of_this_month = today.replace(day=1)
    first_of_prev_month_date = (
        first_of_this_month - datetime.timedelta(days=1)
    ).replace(day=1)
    start_date = datetime.datetime.combine(
        first_of_prev_month_date, datetime.time.min
    )
    end_date = datetime.datetime.combine(
        today + datetime.timedelta(days=1), datetime.time.min
    )

    if is_odinass:
        start_date = start_date.replace(year=start_date.year + 2000)
        end_date = end_date.replace(year=end_date.year + 2000)
    return start_date, end_date

def convert_hex_to_bytes(val: str) -> bytes:
    """converts hex from ms sql like 0x into bytes for SQLAlchemy
    """
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    if val_str.startswith('0x') or val_str.startswith('0X'):
        val_str = val_str[2:]
    return bytes.fromhex(val_str)


#region UFO (ai detected)
import csv
import re

def determine_level(code):
    if not code:
        return 1
    clean_code = code.strip('.')
    if not clean_code:
        return 1
    return clean_code.count('.') + 1

def generate_hex_id(index):
    hex_str = format(index + 1, 'X').zfill(32)
    return f"0x{hex_str}"

def process_source_file(input_filename, output_filename):
    rows = []
    stack = {}
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError as fnf:
        print(f"exception: {fnf}")
        return

    raw_data = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        
        if len(parts) == 2 and (re.match(r'^\d+(\.\d+)*\.?$', parts[0]) or parts[0].replace('.', '').isdigit()):
            code = parts[0]
            name = parts[1].strip('"')
        else:
            code = ""
            name = line.strip('"')
            
        level = determine_level(code)
        raw_data.append((code, name, level))

   
    for idx, (code, name, level) in enumerate(raw_data):
        row_id = generate_hex_id(idx)
        

        parent_id = "NULL"
        if level > 1:
       
            for l in range(level - 1, 0, -1):
                if l in stack:
                    parent_id = stack[l]
                    break
        
        stack[level] = row_id
    
        for l in list(stack.keys()):
            if l > level:
                del stack[l]
                
        rows.append([row_id, parent_id, code, name])

   
    with open(output_filename, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["ID", "ParentID", "Code", "Name"])
        writer.writerows(rows)
#endregion