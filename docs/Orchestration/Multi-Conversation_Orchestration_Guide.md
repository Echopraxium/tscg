# Multi-Conversation Orchestration with Claude AI Pro

## Overview

This guide explains how to orchestrate the TSCG framework development using multiple Claude AI Pro conversations, with you acting as the human orchestrator (the "bus" between specialized agents).

---

## 🎭 Architecture Pattern: "Human-in-the-Loop Orchestration"

```
YOU (Human Orchestrator)
    ↓
┌───────────────────────────────────────────┐
│  Conversation 1: "Ontology Expert"       │
│  Conversation 2: "Backend Architect"     │
│  Conversation 3: "Frontend Architect"    │
│  Conversation 4: "QA Officer"            │
│  Conversation 5: "Compilation Analyser"  │
└───────────────────────────────────────────┘
```

You act as the **communication bus** between agents.

---

## 🚀 Step-by-Step Setup

### Step 1: Create Specialized Conversations

Create **5-7 Claude AI Pro conversations** with clear names:

1. **"TSCG - Ontology Expert"**
2. **"TSCG - Backend Architect"**
3. **"TSCG - Frontend Architect"**
4. **"TSCG - Orchestrator Architect"**
5. **"TSCG - QA Officer"**
6. **"TSCG - Compilation Analyser"**
7. **"TSCG - Reboot Kit Manager"**

---

### Step 2: Initialize Each Conversation

**In each conversation, start with:**

```markdown
You are the [ROLE] for the TSCG project.

[Paste the corresponding role-prompt content from role-prompts/*.md]

PROJECT CONTEXT:
[Paste Smart_Prompt_M3_M2_Updated.md]

AVAILABLE FILES:
[Paste files.txt]

Please confirm you understand your role and are ready to work.
```

**Use Claude's Memory Feature:**
- Go to conversation settings
- Enable "Generate memory from chat history"
- Claude will automatically remember its role

---

### Step 3: Orchestration Workflow

#### Example: Creating a New M1 Concept

**Sequence:**

```
┌─────────────────────────────────────────────────┐
│ 1. YOU → Ontology Expert                       │
│    "Define the M1 concept 'Financial Option'"  │
└─────────────────────────────────────────────────┘
           ↓ (Receive JSON-LD definition)
┌─────────────────────────────────────────────────┐
│ 2. YOU → Backend Architect                     │
│    "Here is the Ontology Expert's definition:" │
│    [Paste JSON-LD definition]                  │
│    "Generate the corresponding F# type"        │
└─────────────────────────────────────────────────┘
           ↓ (Receive F# code)
┌─────────────────────────────────────────────────┐
│ 3. YOU → Compilation Analyser                  │
│    "Here is the new F# code:"                  │
│    [Paste code]                                │
│    "Verify compilation"                        │
└─────────────────────────────────────────────────┘
           ↓ (Receive feedback)
┌─────────────────────────────────────────────────┐
│ 4. YOU → Frontend Architect                    │
│    "Here is the validated F# type:"            │
│    [Paste code]                                │
│    "Create the UI visualizer"                  │
└─────────────────────────────────────────────────┘
           ↓ (Receive UI code)
┌─────────────────────────────────────────────────┐
│ 5. YOU → QA Officer                            │
│    "Here is the complete set (ontology + backend + UI)" │
│    "Validate M2/M3 compliance"                 │
└─────────────────────────────────────────────────┘
```

---

### Step 4: Orchestration Helper Tools

#### A) Transfer Template

Create a `transfer-template.md` file:

```markdown
# Transfer: [SOURCE_AGENT] → [DEST_AGENT]
## Context
Task: [Task description]
Step: [X/Y in workflow]

## Previous Output
[Paste output from previous agent]

## Request
[Your request for this agent]

## Constraints
- Respect coding standards
- Stay within your domain of responsibility
```

#### B) Workflow State Tracking

Maintain a `workflow-state.md` file:

```markdown
# TSCG Workflow State

## Current Task: Implement Financial Option M1 Concept

### Progress
- [x] Ontology definition (Ontology Expert)
- [x] F# type generation (Backend Architect)
- [ ] Compilation validation (Compilation Analyser)
- [ ] UI component (Frontend Architect)
- [ ] QA validation (QA Officer)

### Artifacts
- ontology/m1/financial-option.jsonld
- backend/M1/FinancialOption.fs
```

---

## 💡 Efficiency Tips

### 1. Use Claude Projects (if available)

If you have access to **Projects** in Claude AI Pro:
- Create a "TSCG" project
- Upload all context files (ontologies, docs)
- All conversations in this project will have access to the context

### 2. Tagging System

In your requests, use clear tags:

```
[ONTOLOGY-REQUEST-001]
Define the Financial Option concept

[BACKEND-REQUEST-001]
Input: [ONTOLOGY-REQUEST-001 output]
Generate the F# type
```

### 3. Temporary Conversations

For ad-hoc tasks:
- **"TSCG - Workspace"**: Scratch conversation for quick tests
- **"TSCG - Debug"**: For solving specific problems

### 4. Output Archiving

Systematically save outputs to your repo:

```
outputs/
├── session-2025-01-16/
│   ├── ontology-expert/
│   │   └── financial-option.jsonld
│   ├── backend-architect/
│   │   └── FinancialOption.fs
│   └── workflow-log.md
```

---

## 📋 Startup Checklist

- [ ] Create 5-7 named conversations
- [ ] Initialize each conversation with its role-prompt
- [ ] Upload `Smart_Prompt_M3_M2_Updated.md` to each
- [ ] Upload `files.txt` for repo access
- [ ] Test a simple workflow (1 M1 concept)
- [ ] Document your orchestration process
- [ ] Create transfer templates

---

## 🎯 Advantages of This Approach

✅ **No API costs**: Uses your existing Pro subscription
✅ **Persistent context**: Claude's memory maintains roles
✅ **Flexibility**: You control the workflow
✅ **Easy debugging**: You see every step
✅ **No orchestration code**: No need to code the coordinator

---

## ⚠️ Limitations vs API

❌ **No automation**: Manual copy-paste required
❌ **Slower**: Each step requires your intervention
❌ **No parallelization**: One agent at a time
❌ **Manual state management**: You must track progress

But for an R&D project like TSCG where you want to **understand and validate each step**, this is perfect! 🎯

---

## 🔧 Practical Example: Full Workflow

### Task: Create "Market Order" M1 Concept for Finance Extension

#### Session 1: Ontology Expert

**Your prompt:**
```
Define a new M1 concept: "Market Order" for a Financial Markets extension.

Requirements:
- Must inherit from M2 metaconcepts
- Tensor signature must be valid
- Provide JSON-LD definition

Context: Market Order is a directive to buy/sell a security at the best available current price.
```

**Expected output:** JSON-LD file defining MarketOrder with proper M2/M3 links

---

#### Session 2: Backend Architect

**Your prompt:**
```
Here is the Ontology Expert's definition for MarketOrder:

[PASTE JSON-LD]

Generate the F# domain type that:
1. Implements the tensorial signature
2. Provides type-safe construction
3. Includes validation rules
4. Follows TSCG coding standards
```

**Expected output:** `MarketOrder.fs` with complete F# type

---

#### Session 3: Compilation Analyser

**Your prompt:**
```
Verify this F# code compiles correctly:

[PASTE MarketOrder.fs]

Project context:
- Target: .NET 8.0
- Dependencies: FSharp.Core, TSCP.Core.M3
- Check for: syntax errors, type safety, namespace correctness
```

**Expected output:** Compilation report + fixes if needed

---

#### Session 4: Frontend Architect

**Your prompt:**
```
Create a Fable component to visualize MarketOrder instances.

F# Type definition:
[PASTE validated MarketOrder.fs]

Requirements:
- Display tensor signature components (A, S, F, I, D)
- Show M2 parent relationships
- Interactive state inspection
- Use Feliz for UI
```

**Expected output:** `MarketOrderVisualizer.fs` Fable component

---

#### Session 5: QA Officer

**Your prompt:**
```
Validate the complete MarketOrder implementation:

1. Ontology: [PASTE JSON-LD]
2. Backend: [PASTE MarketOrder.fs]
3. Frontend: [PASTE MarketOrderVisualizer.fs]

Verify:
- M3 orthogonality compliance
- M2 tensor signature correctness
- Type safety across layers
- Coding standards compliance
```

**Expected output:** Validation report + checklist

---

## 📚 Reference: Role Descriptions

### Ontology Expert
- **Focus**: M1 concept definitions, JSON-LD generation
- **Input**: Concept requirements, domain context
- **Output**: JSON-LD ontology files
- **Key skill**: Ensuring M2/M3 compliance

### Backend Architect
- **Focus**: F# domain model implementation
- **Input**: JSON-LD definitions
- **Output**: F# types, validation logic
- **Key skill**: Type-safe tensorial signatures

### Frontend Architect
- **Focus**: UI components for concept visualization
- **Input**: F# types
- **Output**: Fable/Blazor components
- **Key skill**: Making abstract math concepts tangible

### Orchestrator Architect
- **Focus**: Project structure, integration
- **Input**: Independent backend/frontend work
- **Output**: .sln files, shared contracts, DI setup
- **Key skill**: Making components work together

### QA Officer
- **Focus**: Validation, compliance checking
- **Input**: Complete artifacts from all layers
- **Output**: Validation reports, test suites
- **Key skill**: Verifying M2/M3 mathematical correctness

### Compilation Analyser
- **Focus**: Build issues, error resolution
- **Input**: Code that fails to compile
- **Output**: Error analysis, fixes
- **Key skill**: Debugging complex type errors

### Reboot Kit Manager
- **Focus**: Documentation, onboarding
- **Input**: Working implementations
- **Output**: README files, tutorials, architecture docs
- **Key skill**: Making the system understandable

---

## 🎓 Best Practices

### DO's ✅
- Always include full context in transfers
- Keep workflow state updated
- Archive all outputs systematically
- Use clear tagging for traceability
- Validate before moving to next step
- Document decisions and rationale

### DON'Ts ❌
- Don't skip QA validation
- Don't lose track of which conversation is which
- Don't forget to update files.txt when repo changes
- Don't mix roles (keep conversations specialized)
- Don't proceed if compilation fails
- Don't forget coding standards (UUID, comments, etc.)

---

## 🔄 Iteration Pattern

When an agent's output needs revision:

```
1. Identify the issue
2. Go back to responsible agent
3. Provide specific feedback
4. Request revision
5. Re-validate
6. Continue workflow
```

**Example:**
```
YOU → Backend Architect: "The F# type is missing validation for negative quantities. 
Please add a private constructor with validation."

Backend Architect → YOU: [Revised code with validation]

YOU → Compilation Analyser: "Re-verify this updated code"
```

---

## 📊 Progress Tracking Template

```markdown
# TSCG Development Log

## Session: [DATE]

### Concepts Completed
- [ ] Concept A
- [ ] Concept B

### Active Workflows
- Concept C: Step 3/5 (Backend → Compilation)

### Blockers
- None

### Next Session Goals
- Complete Concept C
- Start Concept D (Ontology phase)

### Notes
- Backend Architect suggested optimization for tensor calculations
- Need to update M2 ontology with new category
```

---

## 🚀 Getting Started Today

1. **Open 5 Claude AI Pro tabs**
2. **Name each conversation** (use browser tabs or Claude's conversation naming)
3. **Copy the relevant role-prompt** to each
4. **Upload your Smart_Prompt file**
5. **Test with a simple task**: "Hello, confirm your role"
6. **Run your first workflow** with a simple M1 concept

---

## 💪 You're Ready!

You now have a complete guide to orchestrate TSCG development using Claude AI Pro conversations. This approach gives you:

- **Full control** over the development process
- **Deep understanding** of each step
- **Validation** at every stage
- **No additional costs** beyond your Pro subscription

Start with one simple M1 concept and iterate from there. Good luck! 🎯

---

## 📎 Appendix: Quick Command Templates

### Ontology Expert Prompt Template
```
Define M1 concept: [CONCEPT_NAME]

Domain: [DOMAIN]
Description: [DESCRIPTION]
Parent M2 concepts: [M2_LIST]

Requirements:
- Provide JSON-LD definition
- Specify tensor signature
- Include examples
- Ensure M3 orthogonality
```

### Backend Architect Prompt Template
```
Generate F# type for: [CONCEPT_NAME]

Ontology definition:
[PASTE JSON-LD]

Requirements:
- Implement tensorial signature
- Add validation
- Follow coding standards (UUID, comments, English)
- Include usage examples
```

### Frontend Architect Prompt Template
```
Create visualizer for: [CONCEPT_NAME]

F# Type:
[PASTE TYPE DEFINITION]

Requirements:
- Display tensor components
- Show M2 relationships
- Interactive inspection
- Use [TECHNOLOGY: Fable/Blazor]
```

### QA Officer Prompt Template
```
Validate: [CONCEPT_NAME]

Artifacts:
1. Ontology: [PASTE/LINK]
2. Backend: [PASTE/LINK]
3. Frontend: [PASTE/LINK]

Check:
- [ ] M3 compliance
- [ ] M2 tensor correctness
- [ ] Type safety
- [ ] Coding standards
- [ ] Documentation
```

---

**Version:** 1.0  
**Last Updated:** 2025-01-16  
**Author:** TSCG Project  
**License:** BSD-3-Clause
