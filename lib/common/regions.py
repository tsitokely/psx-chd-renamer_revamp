from pathlib import Path

# Map used by lookup and rename modules
REGION_CODE_MAP = {
    "USA": "US", "Japan": "JP", "Europe": "EU", "World": "WD",
    "Asia": "AS", "Korea": "KR", "China": "CN", "Germany": "DE",
    "France": "FR", "Spain": "ES", "Italy": "IT", "Brazil": "BR",
    "Australia": "AU", "Netherlands": "NL", "Sweden": "SE",
}

# Language codes recognized in PSX Datacenter parsing
LANGUAGE_CODES = {
    "En", "Fr", "De", "Es", "It", "Nl", "Pt", "Sv", "No", "Da",
    "Fi", "Zh", "Ja", "Ko", "Ru", "Pl", "El", "Ca", "Cs", "Hr",
    "Hu", "Ar", "He", "Tr", "Th", "Vi", "Id", "Bg", "Ro", "Sk", "Sl", "Uk",
}

# Mappings used by rename module
LANGUAGE_CODE_MAP = {
    "En": "E", "Fr": "F", "De": "G", "Es": "S", "It": "I",
    "Nl": "N", "Pt": "P", "Sv": "Sw", "No": "No", "Da": "Da",
    "Fi": "Fi", "Ja": "J", "Ko": "K", "Zh": "Zh", "Ru": "R", "Pl": "Pl",
}

COUNTRY_REGION_LANGUAGE_MAP = {
    "France": ("EU", "F"),
    "Germany": ("EU", "G"),
    "Spain": ("EU", "S"),
    "Italy": ("EU", "I"),
    "Netherlands": ("EU", "N"),
    "Portugal": ("EU", "P"),
    "Sweden": ("EU", "Sw"),
    "Norway": ("EU", "No"),
    "Denmark": ("EU", "Da"),
    "Finland": ("EU", "Fi"),
    "Poland": ("EU", "Pl"),
    "Russia": ("EU", "R"),
    "Greece": ("EU", "Gr"),
    "Korea": ("AS", "K"),
    "China": ("AS", "Zh"),
    "Taiwan": ("AS", "Zh"),
    "Australia": ("AU", "E"),
    "Brazil": ("US", "Pt"),
    "Japan": ("JP", "J"),
}

__all__ = [
    "REGION_CODE_MAP",
    "LANGUAGE_CODES",
    "LANGUAGE_CODE_MAP",
    "COUNTRY_REGION_LANGUAGE_MAP",
]
