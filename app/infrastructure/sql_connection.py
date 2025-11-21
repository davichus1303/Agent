import pyodbc
import asyncio
from typing import Dict, Any

class SQLConnection:

    def __init__(self):
        self.connection_string = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=localhost,1433;"
            "Database=master;"
            "UID=sa;"
            "PWD=paswordOfSQLsa;"
            "TrustServerCertificate=yes;"
        )

    async def run_stored_procedure(self, sp_name: str, params: Dict[str, Any]):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._exec_proc_sync, sp_name, params)

    def _exec_proc_sync(self, sp_name: str, params: Dict[str, Any]):
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        param_str = ", ".join([f"{k}='{v}'" for k, v in params.items()])
        query = f"EXEC {sp_name} {param_str}"

        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

        return