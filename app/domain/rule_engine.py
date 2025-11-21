from typing import Dict, Any, Optional, List

# A class for matching payloads against rules.
# Attributes:
#     rules: The list of rules to match against.
class RuleEngine:

    # Constructor method. Initializes the rule engine with a list of rules.
    def __init__(self, rules: List[Dict[str, Any]]):
        self.rules = rules

    # Public method to match the payload against the rule criteria.
    # Returns the first matching rule, or None if no match is found.
    def match(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Match the payload against the rule criteria.
        """
        for rule in self.rules:
            match_criteria = rule.get("match_criteria", {})
            if all(payload.get(k) == v for k, v in match_criteria.items()):
                return rule
        return None
