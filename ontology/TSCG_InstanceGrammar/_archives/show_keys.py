#!/usr/bin/env python3
"""Quick diagnostic - show exact keys in scores"""
import json
from pathlib import Path

file_path = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg/instances/poclets/FireTriangle/M0_FireTriangle.jsonld")

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

ontology = data["@graph"][0]

print("ASFID keys:", list(ontology["m0:asfidScores"].keys()))
print("REVOI keys:", list(ontology["m0:revoiScores"].keys()))
