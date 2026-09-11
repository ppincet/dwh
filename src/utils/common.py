import datetime
import pandas as pd

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

def get_rolling_window_standard(is_odinass: bool):
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
'''
    converts hex from ms sql like 0x into bytes for SQLAlchemy
'''
def convert_hex_to_bytes(val: str) -> bytes:
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    if val_str.startswith('0x') or val_str.startswith('0X'):
        val_str = val_str[2:]
    return bytes.fromhex(val_str)



def find_subkontos() -> None:
    data = {
        "col": [
            "Справочник.ПрибылиУбытки",
            "Перечисление.БазаОборотныхНалогов.Дополнительно", # строка с двумя точками для теста
            "Справочник.СтавкиУСН"
        ]
    }
    df = pd.DataFrame(data)

    # Извлекаем текст после первой точки до второй точки (или до конца)
    df['result'] = df['col'].str.extract(r'\.([^.]+)', expand=False)

    print(df)