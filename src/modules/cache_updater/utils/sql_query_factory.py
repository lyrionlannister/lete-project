from config.app import Logger
from typing import Any
from sqlalchemy import text, TextClause

class SqlQueryFactory:
    _logger = Logger.get_logger()

    
    @classmethod
    async def create_select_query(
        cls,
        table_name: str,
        columns: list[str],
        conditions: dict[str, Any] | None = None
    ) -> tuple[TextClause, dict]:
        try:
            columns_str = await cls._build_columns(columns)
            query = f"SELECT {columns_str} FROM {table_name}"

            where_clause, params = await cls._build_conditions(conditions)
            if where_clause:
                query += " WHERE " + where_clause

            query += ";"
            return text(query), params
        except Exception as e:
            cls._logger.error(f"Error creating select query: {e}")
            raise RuntimeError(f"Error creating select query: {e}")

    

    @staticmethod
    async def _build_columns(columns: list[str]) -> str:
        return ", ".join(columns) if columns else "*"

    @classmethod
    async def _build_conditions(cls, conditions: dict[str, Any] | None) -> tuple[str, dict]:
        if not conditions:
            return "", {}

        condition_strs, params = [], {}
        for key, value in conditions.items():
            sql, param_values = await cls._build_condition(key, value)
            condition_strs.append(sql)
            params.update(param_values)

        return " AND ".join(condition_strs), params

    @staticmethod
    async def _build_condition(key: str, value: Any) -> tuple[str, dict]:
        
        if isinstance(value, tuple) and len(value) == 2 and value[0] == "between":
            start, end = value[1]
            sql = f"{key} BETWEEN :{key}_start AND :{key}_end"
            return sql, {f"{key}_start": start, f"{key}_end": end}

        sql = f"{key} = :{key}"
        return sql, {key: value}
