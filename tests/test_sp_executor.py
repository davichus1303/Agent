import pytest
from unittest.mock import patch, MagicMock
from app.services.sp_executor import SPExecutor

# Test explicit mapping
@pytest.mark.asyncio
async def test_explicit_mapping():
    rule = {
        "target_action": {
            "name": "sp_insert_transaction",
            "mapping_strategy": "explicit",
            "params_map": {
                "@ref_external": "transaction_id",
                "@amount": "total_amount",
                "@currency": "currency_code"
            }
        }
    }

    payload = {
        "transaction_id": "TX-1",
        "total_amount": 100.5,
        "currency_code": "USD"
    }

    with patch("app.infrastructure.sql_connection.SQLConnection.run_stored_procedure") as mock_exec:
        await SPExecutor.execute(rule, payload)

        mock_exec.assert_called_once()
        args = mock_exec.call_args[0]
        
        assert args[0] == "sp_insert_transaction"
        assert args[1] == {
            "@ref_external": "TX-1",
            "@amount": 100.5,
            "@currency": "USD"
        }

@pytest.mark.asyncio
# Test pass-through mapping
async def test_pass_through_mapping():
    rule = {
        "target_action": {
            "name": "sp_update_inventory",
            "mapping_strategy": "pass_through"
        }
    }

    payload = {"abc": 123}

    with patch("app.infrastructure.sql_connection.SQLConnection.run_stored_procedure") as mock_exec:
        await SPExecutor.execute(rule, payload)

        args = mock_exec.call_args[0]
        
        assert args[0] == "sp_update_inventory"
        assert "@payload" in args[1]
        assert '{"abc": 123}' in args[1]["@payload"]
