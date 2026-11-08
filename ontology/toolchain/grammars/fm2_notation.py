#!/usr/bin/env python3
"""
fm2_notation.py — parser of the combo-formula notation (Fm2 / Fm1m2) and
generator of its SHACL pattern.

Author : Echopraxium with the collaboration of Claude AI
Version: 1.0.0 (2026-11-08)
Home   : ontology/toolchain/grammars/fm2_notation.py

The grammar is Fm2_notation.ebnf, next to this file: it is the single source.
This module follows it production by production (one function per production,
same names), and builds the SHACL pattern from the SAME token definitions, so
the parser and the pattern cannot drift apart; tests/test_fm2_notation.py checks
both against the examples of the EBNF.

    python fm2_notation.py "Fm2(Component, Process, Trajectory { properties: [shape: Circular, final: true] })"
    python fm2_notation.py --shacl-pattern
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field

# ── tokens: shared by the parser and the SHACL pattern ─────────────────────────
FUNCTION = r"Fm2²|Fm2|Fm1m2"
CONCEPT_NAME = r"[A-Z][A-Za-z0-9]*"
PROPERTY_NAME = r"[A-Za-z][A-Za-z0-9_]*"
PROPERTY_VALUE = r"[A-Za-z][A-Za-z0-9_\-]*"
BOOLEAN = r"true|false"
MEASURE = r"[a-z][A-Za-z0-9_]*"
DIMENSION = r"St|Ss|It|Im|A|S|F|I|D|R|E|V|O|T|K|L"
RELOP = r"<<|>>|<=|>=|<|>|=|≠"
WS = r"[ \t]*"


@dataclass
class PropertyBinding:
    name: str
    value: str
    final: bool = False


@dataclass
class Reference:
    concept: str | None      # None = the argument carrying the block
    dimension: str


@dataclass
class Relation:
    left: tuple              # (measure or None, Reference)
    op: str
    right: tuple
    text: str


@dataclass
class Argument:
    name: str
    properties: list = field(default_factory=list)
    constraints: list = field(default_factory=list)
    has_block: bool = False


@dataclass
class Formula:
    function: str
    arguments: list
    trailing: str = ""       # text after the closing parenthesis (a guard: GCC009)

    @property
    def names(self):
        return [a.name for a in self.arguments]


class NotationError(ValueError):
    def __init__(self, msg, pos, text):
        super().__init__(f"{msg} at column {pos + 1}: …{text[pos:pos + 30]}")
        self.pos = pos


class _Parser:
    def __init__(self, text):
        self.t, self.i = text, 0

    # helpers
    def ws(self):
        self.i = re.compile(WS).match(self.t, self.i).end()

    def tok(self, pattern, what):
        self.ws()
        m = re.compile(f"(?:{pattern})").match(self.t, self.i)
        if not m:
            raise NotationError(f"expected {what}", self.i, self.t)
        self.i = m.end()
        return m.group(0)

    def lit(self, s):
        self.ws()
        if not self.t.startswith(s, self.i):
            raise NotationError(f"expected '{s}'", self.i, self.t)
        self.i += len(s)

    def peek(self, s):
        self.ws()
        return self.t.startswith(s, self.i)

    # productions (same names as in Fm2_notation.ebnf)
    def formula(self, allow_trailing):
        fn = self.tok(FUNCTION, "Fm2 / Fm1m2")
        self.lit("(")
        args = [self.argument()]
        while self.peek(","):
            self.lit(",")
            args.append(self.argument())
        self.lit(")")
        rest = self.t[self.i:].strip()
        if rest and not allow_trailing:
            raise NotationError("nothing may follow the signature", self.i, self.t)
        return Formula(fn, args, rest)

    def argument(self):
        a = Argument(self.tok(CONCEPT_NAME, "a concept name"))
        if self.peek("{"):
            self.block(a)
        return a

    def block(self, a):
        a.has_block = True
        self.lit("{")
        if self.peek("properties"):
            a.properties = self.properties()
            if self.peek(","):
                self.lit(",")
                a.constraints = self.constraints()
        elif self.peek("constraints"):
            a.constraints = self.constraints()
        else:
            raise NotationError("expected 'properties' or 'constraints'", self.i, self.t)
        self.lit("}")

    def properties(self):
        self.lit("properties")
        self.lit(":")
        self.ws()
        if self.t.startswith("[[", self.i) or re.match(r"\[" + WS + r"\[", self.t[self.i:]):
            return self.property_list()
        return [self.property_tuple()]

    def property_list(self):
        self.lit("[")
        out = [self.property_tuple()]
        while self.peek(","):
            self.lit(",")
            out.append(self.property_tuple())
        self.lit("]")
        return out

    def property_tuple(self):
        self.lit("[")
        name = self.tok(PROPERTY_NAME, "a property name")
        self.lit(":")
        value = self.tok(PROPERTY_VALUE, "a property value")
        final = False
        if self.peek(","):
            self.lit(",")
            self.lit("final")
            self.lit(":")
            final = self.tok(BOOLEAN, "true / false") == "true"
        self.lit("]")
        return PropertyBinding(name, value, final)

    def constraints(self):
        self.lit("constraints")
        self.lit(":")
        self.lit("[")
        out = [self.relation()]
        while self.peek(","):
            self.lit(",")
            out.append(self.relation())
        self.lit("]")
        return out

    def relation(self):
        self.ws()
        start = self.i
        left = self.term()
        op = self.tok(RELOP, "a relation (<<, <, =, …)")
        right = self.term()
        return Relation(left, op, right, self.t[start:self.i].strip())

    def term(self):
        self.ws()
        m = re.compile(f"({MEASURE}){WS}\\(").match(self.t, self.i)
        if m:
            self.i = m.end()
            ref = self.reference()
            self.lit(")")
            return (m.group(1), ref)
        return (None, self.reference())

    def reference(self):
        self.ws()
        m = re.compile(f"({CONCEPT_NAME})\\.").match(self.t, self.i)
        concept = None
        if m:
            concept, self.i = m.group(1), m.end()
        dim = self.tok(f"(?:{DIMENSION})(?![A-Za-z0-9])", "a dimension")
        return Reference(concept, dim)


def parse(text, allow_trailing=False):
    """Parse a combo formula. With allow_trailing=True, text after the closing
    parenthesis is returned in Formula.trailing instead of raising (so that the
    checker can report a guard as GCC009 and still check the signature)."""
    return _Parser(text.strip()).formula(allow_trailing)


def shacl_pattern():
    """The sh:pattern of the whole notation, built from the same tokens."""
    g = lambda p: f"({p})"
    tup = (r"\[" + WS + g(PROPERTY_NAME) + WS + ":" + WS + g(PROPERTY_VALUE) + WS
           + g("," + WS + "final" + WS + ":" + WS + g(BOOLEAN) + WS) + r"?\]")
    props = ("properties" + WS + ":" + WS
             + g(tup + "|" + r"\[" + WS + tup + g(WS + "," + WS + tup) + "*" + WS + r"\]"))
    ref = g(CONCEPT_NAME + r"\.") + "?" + g(DIMENSION)
    term = g(MEASURE + WS + r"\(" + WS + ref + WS + r"\)" + "|" + ref)
    rel = term + WS + g(RELOP) + WS + term
    cons = "constraints" + WS + ":" + WS + r"\[" + WS + rel + g(WS + "," + WS + rel) + "*" + WS + r"\]"
    block = r"\{" + WS + g(props + g(WS + "," + WS + cons) + "?" + "|" + cons) + WS + r"\}"
    arg = CONCEPT_NAME + g(WS + block) + "?"
    return "^" + g(FUNCTION) + r"\(" + WS + arg + g(WS + "," + WS + arg) + "*" + WS + r"\)$"


if __name__ == "__main__":
    if sys.argv[1:] == ["--shacl-pattern"]:
        print(shacl_pattern())
    else:
        for s in sys.argv[1:]:
            print(parse(s))
