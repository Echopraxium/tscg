"""
TSCG Engine Core - Data models and ontology loading

Author: Echopraxium with the collaboration of Claude AI
"""

from .models import (
    ASFIDScore,
    REVOIScore,
    Metaconcept,
    Poclet,
    OntologyMetadata,
    ValueSpaceAttribute
)
from .ontology_loader import OntologyLoader

__all__ = [
    'ASFIDScore',
    'REVOIScore',
    'Metaconcept',
    'Poclet',
    'OntologyMetadata',
    'ValueSpaceAttribute',
    'OntologyLoader'
]
