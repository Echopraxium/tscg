# TSCG Instance Pipeline — Deployment Guide

## 📦 Files to Deploy

This package contains:
1. `SKILL.md` — English version of the renamed tscg-instance-pipeline skill
2. `validate_m0_instance.py` — Standalone SHACL validation script

## 🎯 Deployment Steps

### 1. Deploy the Skill File

**Location in TSCG repo:**
```
.claude/skills/tscg-instance-pipeline/SKILL.md
```

**Actions:**
```bash
# Navigate to your TSCG repo
cd /path/to/tscg

# Create the skill directory (if renaming from tscg-poclet-pipeline)
mv .claude/skills/tscg-poclet-pipeline .claude/skills/tscg-instance-pipeline

# Copy the new English SKILL.md
cp /path/to/downloaded/SKILL.md .claude/skills/tscg-instance-pipeline/SKILL.md
```

**Alternative (if starting fresh):**
```bash
# Create new skill directory
mkdir -p .claude/skills/tscg-instance-pipeline

# Copy the SKILL.md
cp /path/to/downloaded/SKILL.md .claude/skills/tscg-instance-pipeline/SKILL.md
```

### 2. Deploy the Validation Script

**Location in TSCG repo:**
```
ontology/TSCG_Grammar/validate_m0_instance.py
```

**Actions:**
```bash
# Navigate to TSCG Grammar directory
cd /path/to/tscg/ontology/TSCG_Grammar

# Copy the validation script
cp /path/to/downloaded/validate_m0_instance.py .

# Make it executable (Linux/Mac)
chmod +x validate_m0_instance.py
```

**Verify deployment:**
```bash
# Check file structure
ls -l ontology/TSCG_Grammar/
# Should show:
# - M0_Instances_Schema.shacl.ttl
# - validate_m0_instance.py
```

### 3. Install Dependencies

**Required Python package:**
```bash
pip install pyshacl --break-system-packages
```

**Verify installation:**
```bash
python -c "import pyshacl; print(pyshacl.__version__)"
```

### 4. Test the Validation Script

**Test with an existing compliant instance (should pass):**
```bash
# From TSCG repo root
python ontology/TSCG_Grammar/validate_m0_instance.py instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

**Expected output:**
```
======================================================================
TSCG M0 INSTANCE SHACL VALIDATION
======================================================================

📄 Instance file: instances/poclets/FireTriangle/M0_FireTriangle.jsonld
📋 Schema file:   ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl

======================================================================

✅ VALIDATION PASSED - Instance conforms to TSCG SHACL grammar

======================================================================
```

### 5. Sync the Skill with Claude.ai

**Option A: Via Claude.ai web interface**
1. Go to Claude.ai → Skills
2. Find "tscg-instance-pipeline" (or create it)
3. Paste the content of `SKILL.md`
4. Save

**Option B: Via .claude directory sync (if using Claude Code)**
- The skill should auto-sync from `.claude/skills/tscg-instance-pipeline/SKILL.md`

### 6. Update Git Repository

```bash
# Stage the new/renamed files
git add .claude/skills/tscg-instance-pipeline/SKILL.md
git add ontology/TSCG_Grammar/validate_m0_instance.py

# Remove old skill if renamed
git rm -r .claude/skills/tscg-poclet-pipeline

# Commit
git commit -m "feat: Rename tscg-poclet-pipeline → tscg-instance-pipeline (English)

- Translate complete skill to English
- Add mandatory SHACL validation step (3.5) in Modeling phase
- Add standalone validation script in ontology/TSCG_Grammar/
- Update all references to 'poclet' → 'instance' terminology"

# Push
git push origin main
```

## 📋 Post-Deployment Checklist

- [ ] `SKILL.md` deployed in `.claude/skills/tscg-instance-pipeline/`
- [ ] `validate_m0_instance.py` deployed in `ontology/TSCG_Grammar/`
- [ ] `pyshacl` installed and tested
- [ ] Validation script tested on FireTriangle (passes)
- [ ] Skill synced with Claude.ai
- [ ] Changes committed to Git
- [ ] Old `tscg-poclet-pipeline` directory removed (if applicable)

## 🔄 Changes Summary

### Skill Renaming
- **Old name:** `tscg-poclet-pipeline`
- **New name:** `tscg-instance-pipeline`
- **Rationale:** More accurate terminology (instances > poclets)

### Translation
- **Source language:** French
- **Target language:** English
- **Scope:** Complete translation of all sections

### New Feature: SHACL Validation (Step 3.5)
- **Location in pipeline:** Between JSON-LD generation (3.3) and Simulation (4)
- **Requirement:** MANDATORY — must pass before proceeding
- **Script:** `ontology/TSCG_Grammar/validate_m0_instance.py`
- **Blocking:** If validation fails repeatedly → sync point ⏸ with Michel

### Technical Improvements
- Standalone validation script (no dependency on migration tools)
- Clear error messages with common fixes table
- Exit codes for automation (0 = success, 1 = failure)
- Auto-detection of SHACL schema location

## 🆘 Troubleshooting

### Issue: "pyshacl command not found"
**Solution:**
```bash
pip install pyshacl --break-system-packages
```

### Issue: "SHACL schema file not found"
**Solution:**
- Ensure you're running the script from TSCG repo root
- Verify `ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl` exists
- Use `--schema` argument to specify custom path

### Issue: "Validation fails with namespace errors"
**Common cause:** Relative URLs in @context instead of absolute URLs

**Fix:** Replace in JSON-LD:
```json
// ❌ WRONG (relative)
"m3": "M3_GenesisSpace.jsonld#"

// ✅ CORRECT (absolute)
"m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#"
```

### Issue: Skill doesn't trigger in Claude.ai
**Solutions:**
1. Check skill description matches use cases (mentions "instance", "TSCG", "model", etc.)
2. Re-upload skill to Claude.ai Skills interface
3. Test with explicit trigger phrase: "Create a TSCG instance for..."

## 📚 Related Documentation

- **SHACL Schema:** `ontology/TSCG_Grammar/M0_Instances_Schema.shacl.ttl`
- **M2 Formulas Reference:** `docs/reboot-kit/M2_FormulasReference_v15.10.0.md`
- **Smart Prompt:** `docs/reboot-kit/SmartPrompts/Smart_Prompt_M3_M2_Updated.md`
- **Reference Instance:** `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`

---

**Last updated:** 2026-04-20
**Version:** 1.0.0
**Author:** Echopraxium with the collaboration of Claude AI
