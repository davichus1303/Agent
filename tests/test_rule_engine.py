import pytest
from app.domain.rule_engine import RuleEngine

# Fixture for rules
@pytest.fixture
def rules():
    return [
        {
            "domain_id": "FINANCE_PARTNER_X",
            "match_criteria": {"source_system": "SAP_CLOUD"},
            "target_action": {"name": "sp_insert_transaction"}
        },
        {
            "domain_id": "LOGISTICS_V2",
            "match_criteria": {"source_system": "WMS_BOT"},
            "target_action": {"name": "sp_update_inventory"}
        }
    ]

# Test successful rule matching
def test_rule_match_success(rules):
    engine = RuleEngine(rules)
    payload = {"source_system": "SAP_CLOUD"}

    rule = engine.match(payload)

    assert rule is not None
    assert rule["domain_id"] == "FINANCE_PARTNER_X"

# Test failed rule matching
def test_rule_match_failure(rules):
    engine = RuleEngine(rules)
    payload = {"source_system": "UNKNOWN"}

    rule = engine.match(payload)

    assert rule is None
