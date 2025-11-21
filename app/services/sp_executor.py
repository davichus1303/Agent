import json
from typing import Dict, Any
from ..infrastructure.sql_connection import SQLConnection

class SPExecutor:

    @staticmethod
    async def execute(rule: Dict[str, Any], payload: Dict[str, Any]):
        """
        Executes the stored procedure based on the rule.
        """
        sp_name = rule["target_action"]["name"]
        strategy = rule["target_action"]["mapping_strategy"]

        if strategy == "explicit":
            params_map = rule["target_action"]["params_map"]
            params = {db_key: payload.get(src_key) for db_key, src_key in params_map.items()}
        else:
            # pass-through: send full JSON as a string
            params = {"@payload": json.dumps(payload)}

        conn = SQLConnection()
        await conn.run_stored_procedure(sp_name, params)
        await conn.close()