from typing import TypedDict, Optional

class Language(TypedDict):
    id: str
    # This allows situations like the language id being different between piston and monaco
    monacoid: Optional[str]
    name: str
    version: str
