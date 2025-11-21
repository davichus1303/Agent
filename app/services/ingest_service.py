from typing import Dict, Any
from .sp_executor import SPExecutor

class IngestService:

    @staticmethod
    async def process_async(payload: Dict[str, Any], rule: Dict[str, Any]):
        try:
            await SPExecutor.execute(rule, payload)
        except Exception as e:
            # TODO: Add retry logic, DLQ, or structured logging
            print("❌ Error executing SP:", str(e))
            raise
