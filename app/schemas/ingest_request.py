from pydantic import BaseModel
from typing import Any, Dict

# A pydantic BaseModel for representing an ingest request.
# Attributes:
#     __root__: A dictionary containing the ingest request data
class IngestRequest(BaseModel):
    __root__: Dict[str, Any]

# Convert the IngestRequest object to a dictionary
    def to_dict(self) -> Dict[str, Any]:
        return self.__root__
