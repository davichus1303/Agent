import json
from typing import List, Dict, Any

# A class for loading rules from a JSON file.
# Attributes:
#     rules_file: The path to the rules file.
#     rules: The loaded rules.
class RulesLoader:
    # Constructor method. Loads rules from the specified file.
    def __init__(self, rules_file: str):
        self.rules_file = rules_file
        self.rules = self._load_rules()

    # Private method to load rules from the file.
    # Returns a list of rules.  
    def _load_rules(self) -> List[Dict[str, Any]]:
        with open(self.rules_file, "r") as f:
            return json.load(f)

    # Public method to reload rules from the file.
    def reload_rules(self):
        self.rules = self._load_rules()
