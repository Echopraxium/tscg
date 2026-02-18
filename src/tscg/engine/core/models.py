"""
Core data models for TSCG ontologies and metaconcepts

Author: Echopraxium with the collaboration of Claude AI
"""

from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl


class ValueSpaceAttribute(BaseModel):
    """A ValueSpace attribute with its range/domain"""
    name: str
    value_type: Literal["continuous", "discrete", "integer", "categorical"]
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    discrete_values: Optional[List[str]] = None
    unit: Optional[str] = None
    description: Optional[str] = None


class ASFIDScore(BaseModel):
    """ASFID (Eagle Eye - Territory) scores"""
    attractor: float = Field(ge=0.0, le=1.0)
    structure: float = Field(ge=0.0, le=1.0)
    flow: float = Field(ge=0.0, le=1.0)
    information: float = Field(ge=0.0, le=1.0)
    dynamics: float = Field(ge=0.0, le=1.0)
    
    @property
    def overall(self) -> float:
        """Overall ASFID score (average)"""
        return (self.attractor + self.structure + self.flow + 
                self.information + self.dynamics) / 5.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "A": self.attractor,
            "S": self.structure,
            "F": self.flow,
            "I": self.information,
            "D": self.dynamics
        }


class REVOIScore(BaseModel):
    """REVOI (Sphinx Eye - Map) scores
    
    CRITICAL: R = Representability, NOT Reproducibility
    """
    representability: float = Field(ge=0.0, le=1.0)
    evolvability: float = Field(ge=0.0, le=1.0)
    verifiability: float = Field(ge=0.0, le=1.0)
    observability: float = Field(ge=0.0, le=1.0)
    interoperability: float = Field(ge=0.0, le=1.0)
    
    @property
    def overall(self) -> float:
        """Overall REVOI score (average)"""
        return (self.representability + self.evolvability + self.verifiability + 
                self.observability + self.interoperability) / 5.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "R": self.representability,
            "E": self.evolvability,
            "V": self.verifiability,
            "O": self.observability,
            "I": self.interoperability
        }


class Metaconcept(BaseModel):
    """A TSCG metaconcept"""
    uri: str
    label: str
    layer: Literal["M3", "M2", "M1", "M0"]
    perspective: Optional[Literal["EagleEye", "SphinxEye", "Genesis"]] = None
    definition: Optional[str] = None
    value_space: List[ValueSpaceAttribute] = Field(default_factory=list)
    related_concepts: List[str] = Field(default_factory=list)
    tensor_formula: Optional[str] = None


class Poclet(BaseModel):
    """A poclet (proof-of-concept system instance)"""
    name: str
    uri: str
    description: Optional[str] = None
    domain: Optional[str] = None
    instance_count: int = 0
    asfid_scores: Optional[ASFIDScore] = None
    revoi_scores: Optional[REVOIScore] = None
    metaconcepts_used: List[str] = Field(default_factory=list)


class OntologyMetadata(BaseModel):
    """Metadata for a TSCG ontology file"""
    uri: str
    layer: Literal["M3", "M2", "M1", "M0"]
    category: Optional[str] = None
    version: Optional[str] = None
    author: str = "Echopraxium with the collaboration of Claude AI"
    description: Optional[str] = None
    imports: List[str] = Field(default_factory=list)
    triple_count: int = 0
