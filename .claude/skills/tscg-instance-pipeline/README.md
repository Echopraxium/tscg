# TSCG Instance Pipeline Skill

Complete pipeline for creating TSCG Instances (M0 ontologies) with built-in SHACL validation.

## 📄 Skill Definition

See **`SKILL.md`** in this directory for the complete skill specification.

## 🚀 Deployment & Setup

**For complete deployment instructions, see:**

👉 **`ontology/TSCG_Grammar/DEPLOYMENT_GUIDE.md`**

This deployment guide covers:
- ✅ Skill deployment to `.claude/skills/tscg-instance-pipeline/`
- ✅ Validation script deployment to `ontology/TSCG_Grammar/`
- ✅ Dependencies installation (`pyshacl`)
- ✅ Testing procedures with existing instances
- ✅ Git commit recommendations
- ✅ Troubleshooting common issues

## 📦 Required Components

This skill requires two components to be deployed:

### 1. Skill File (this directory)
```
.claude/skills/tscg-instance-pipeline/
├── SKILL.md              ← Skill definition (English)
└── README.md             ← This file
```

### 2. Validation Script (in ontology)
```
ontology/TSCG_Grammar/
├── M0_Instances_Schema.shacl.ttl    ← SHACL grammar schema
├── validate_m0_instance.py          ← Validation script
└── DEPLOYMENT_GUIDE.md              ← Complete deployment guide
```

## ⚡ Quick Start

After deploying both components (see DEPLOYMENT_GUIDE.md):

```bash
# 1. Install dependency
pip install pyshacl --break-system-packages

# 2. Test validation script
python ontology/TSCG_Grammar/validate_m0_instance.py \
    instances/poclets/FireTriangle/M0_FireTriangle.jsonld

# 3. Use the skill in Claude.ai
# Trigger: "Create a TSCG instance for [system]"
```

## 🔄 Migration from Previous Version

If migrating from `tscg-poclet-pipeline`:

```bash
# Rename skill directory
mv .claude/skills/tscg-poclet-pipeline \
   .claude/skills/tscg-instance-pipeline

# Update skill files
cp /path/to/new/SKILL.md .claude/skills/tscg-instance-pipeline/
cp /path/to/new/README.md .claude/skills/tscg-instance-pipeline/

# Remove old from git, add new
git rm -r .claude/skills/tscg-poclet-pipeline
git add .claude/skills/tscg-instance-pipeline
```

## 📚 Key Changes (v2.0)

- **Renamed**: `tscg-poclet-pipeline` → `tscg-instance-pipeline`
- **Language**: French → English
- **New Step 3.5**: Mandatory SHACL validation before simulation
- **New Script**: Standalone validation tool in `ontology/TSCG_Grammar/`

## 🆘 Support

For troubleshooting and detailed setup instructions:
- See `ontology/TSCG_Grammar/DEPLOYMENT_GUIDE.md`
- Check SHACL schema: `ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl`
- Reference instance: `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`

---

**Version:** 2.0.0  
**Last updated:** 2026-04-20  
**Author:** Echopraxium with the collaboration of Claude AI
