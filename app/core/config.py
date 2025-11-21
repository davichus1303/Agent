from pydantic import BaseSettings

class Settings(BaseSettings):
    # Path to the rules file
    RULES_FILE: str = "agent_rules.json"

settings = Settings()
