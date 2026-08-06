from abc import ABC, abstractmethod
from typing import List, Dict, Any

# ==========================================
# 1. Интерфейс Стратегии
# ==========================================

class DdlStrategy(ABC):
    """Абстрактный класс стратегии генерации DDL."""
    
    @abstractmethod
    def generate_create_table(self, metadata: Dict[str, Any]) -> str:
        """Генерирует SQL-скрипт создания таблицы по метаданным."""
        pass


# ==========================================
# 2. Конкретные Стратегии
# ==========================================

class PostgresStrategy(DdlStrategy):
    """Стратегия для PostgreSQL."""
    
    def generate_create_table(self, metadata: Dict[str, Any]) -> str:
        table_name = metadata["table_name"]
        fields = metadata["fields"]
        indices = metadata.get("indices", [])
        
        column_defs = []
        for field_name, field_type in fields.items():
            # В PostgreSQL можно использовать маппинг типов при необходимости
            column_defs.append(f"    {field_name} {field_type}")
            
        columns_sql = ",\n".join(column_defs)
        sql = f"CREATE TABLE {table_name} (\n{columns_sql}\n);\n"
        
        # Генерация индексов для Postgres
        for idx in indices:
            idx_name = idx.get("name", f"idx_{table_name}_{'_'.join(idx['columns'])}")
            cols = ", ".join(idx["columns"])
            sql += f"CREATE INDEX {idx_name} ON {table_name} ({cols});\n"
            
        return sql


class MSSqlStrategy(DdlStrategy):
    """Стратегия для MS SQL Server."""
    
    def generate_create_table(self, metadata: Dict[str, Any]) -> str:
        table_name = metadata["table_name"]
        fields = metadata["fields"]
        indices = metadata.get("indices", [])
        
        column_defs = []
        for field_name, field_type in fields.items():
            # Пример специфики MS SQL: можно обрабатывать автоинкремент или типы
            column_defs.append(f"    [{field_name}] {field_type}")
            
        columns_sql = ",\n".join(column_defs)
        sql = f"CREATE TABLE [{table_name}] (\n{columns_sql}\n);\n"
        
        # Генерация индексов для MS SQL
        for idx in indices:
            idx_name = idx.get("name", f"idx_{table_name}_{'_'.join(idx['columns'])}")
            cols = ", ".join([f"[{c}]" for c in idx["columns"]])
            sql += f"CREATE INDEX [{idx_name}] ON [{table_name}] ({cols});\n"
            
        return sql


# ==========================================
# 3. Контекст
# ==========================================

class TableGenerator:
    """Контекст, использующий стратегию для генерации скрипта."""
    
    def __init__(self, strategy: DdlStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: DdlStrategy) -> None:
        """Позволяет менять стратегию на лету."""
        self._strategy = strategy

    def generate(self, metadata: Dict[str, Any]) -> str:
        return self._strategy.generate_create_table(metadata)


# ==========================================
# 4. Пример использования
# ==========================================

if __name__ == "__main__":
   
    table_metadata = {
        "table_name": "users",
        "fields": {
            "id": "INT PRIMARY KEY",
            "username": "VARCHAR(50) NOT NULL",
            "email": "VARCHAR(100)",
            "created_at": "TIMESTAMP"
        },
        "indices": [
            {
                "name": "idx_users_email",
                "columns": ["email"]
            }
        ]
    }

    print("--- PostgreSQL Script ---")
    pg_strategy = PostgresStrategy()
    generator = TableGenerator(pg_strategy)
    print(generator.generate(table_metadata))

    print("--- MS SQL Server Script ---")
    mssql_strategy = MSSqlStrategy()
    generator.set_strategy(mssql_strategy)
    print(generator.generate(table_metadata))