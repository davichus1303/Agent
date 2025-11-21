from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from ...schemas.ingest_request import IngestRequest
from ...infrastructure.rules_loader import RulesLoader
from ...domain.rule_engine import RuleEngine
from ...services.ingest_service import IngestService
from ...core.config import settings

router = APIRouter()

rules_loader = RulesLoader(settings.RULES_FILE)
rule_engine = RuleEngine(rules_loader.rules)

# Public endpoint for ingesting data.
@router.post("/ingest", status_code=202)
async def ingest_data(request: IngestRequest, background: BackgroundTasks):
    payload = request.to_dict()

    rule = rule_engine.match(payload)
    if not rule:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "message": "No matching rule found"}
        )

    background.add_task(IngestService.process_async, payload, rule)

    return {
        "status": "accepted",
        "rule_applied": rule["domain_id"],
        "message": "Payload queued for processing"
    }

# Public endpoint for listing available rules.
@router.get("/rules")
async def list_rules():
    return {"rules": rules_loader.rules}

# Public endpoint for reloading rules.
@router.post("/rules/reload")
async def reload_rules():
    rules_loader.reload_rules()
    return {"status": "success", "message": "Rules reloaded"}
