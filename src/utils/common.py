import datetime
import pandas as pd
import uuid

def create_session(command: str = "DEFAULT") -> dict:
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

import csv
import re

def determine_level(code):
    """Определяет уровень вложенности по количеству точек в коде (например, '1.1.1' -> уровень 3)."""
    if not code:
        return 1
    # Считаем точки в коде (убираем хвостовые)
    clean_code = code.strip('.')
    if not clean_code:
        return 1
    return clean_code.count('.') + 1

def generate_hex_id(index):
    """Генерирует уникальный 16-байтовый hex-идентификатор формата 0x... для binary(16)."""
    hex_str = format(index + 1, 'X').zfill(32)
    return f"0x{hex_str}"

def process_source_file(input_filename, output_filename):
    rows = []
    stack = {}
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Не найден файл {input_filename}. Создайте его и поместите туда исходные данные.")
        return

    raw_data = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Парсим строку: ожидаем, что первый токен — код (если есть), остальное — имя.
        # Пример: "1.1.1. Продажи через интернет-магазин" или просто имя без кода.
        parts = line.split(maxsplit=1)
        
        if len(parts) == 2 and (re.match(r'^\d+(\.\d+)*\.?$', parts[0]) or parts[0].replace('.', '').isdigit()):
            code = parts[0]
            name = parts[1].strip('"')
        else:
            code = ""
            name = line.strip('"')
            
        level = determine_level(code)
        raw_data.append((code, name, level))

    # Генерация ID и связей ParentID
    for idx, (code, name, level) in enumerate(raw_data):
        row_id = generate_hex_id(idx)
        
        # Поиск родителя по стеку уровней
        parent_id = "NULL"
        if level > 1:
            # Ищем ближайший родительский уровень, который выше текущего
            for l in range(level - 1, 0, -1):
                if l in stack:
                    parent_id = stack[l]
                    break
        
        stack[level] = row_id
        # Очищаем дочерний стек при подъеме наверх
        for l in list(stack.keys()):
            if l > level:
                del stack[l]
                
        rows.append([row_id, parent_id, code, name])

    # Запись в результирующий CSV
    with open(output_filename, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["ID", "ParentID", "Code", "Name"])
        writer.writerows(rows)

    print(f"Готово! Обработано строк: {len(rows)}. Результат сохранен в файл: {output_filename}")