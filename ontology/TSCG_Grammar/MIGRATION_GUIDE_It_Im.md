# Migration Guide: I_asfid/I_revoi → It/Im Nomenclature

**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-04-18  
**Version:** 1.0.0  
**Status:** Production

---

## 📋 Executive Summary

This guide documents the migration from ambiguous `I_asfid`/`I_revoi` keys to the clear **It/Im nomenclature** in TSCG poclets, reflecting the bicephalous Territory/Map architecture.

**Nomenclature:**
- **It** = Information (Territory) - Eagle Eye dimension
- **Im** = Interoperability (Map) - Sphinx Eye dimension

---

## 🎯 Why This Migration?

### Problem
The old nomenclature used `I` (or `I_asfid`/`I_revoi`) for both dimensions, creating ambiguity:
- Which `I` are we talking about - ASFID or REVOI?
- No clear connection to Territory/Map conceptual framework

### Solution
- **ASFID (Eagle Eye/Territory):** A, S, F, **It**, D
- **REVOI (Sphinx Eye/Map):** R, E, V, O, **Im**

**Benefits:**
- ✅ Disambiguates the two "I" dimensions
- ✅ Connects to Territory (t) and Map (m) metaphors
- ✅ Maintains compact notation (1-2 chars)
- ✅ Reinforces bicephalous architecture

---

## 📦 Migration Components

### Files to Update (per poclet)
1. **`M0_PocletName.jsonld`** - Core ontology with scores
2. **`M0_PocletName_README.md`** - Documentation with state vectors
3. **`M0_PocletName.html`** - Interactive simulation (if exists)

### Scripts Provided
1. **`fix_scores_final.py`** - Fixes xsd:float typing issues
2. **`migrate_firetriangle_to_it_im.py`** - Migrates JSON-LD keys
3. **`migrate_readme_html_to_it_im.py`** - Migrates README and HTML

---

## 🔧 Step-by-Step Migration Procedure

### Phase 1: JSON-LD Migration

#### Step 1.1: Fix Float Typing (if needed)
**Problem:** Scores typed as `xsd:double` instead of `xsd:float`

**Detection:**
```bash
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld instances/poclets/PocletName/M0_PocletName.jsonld
```

Look for errors like:
```
Value Node: Literal("0.75", datatype=xsd:double)
Expected: xsd:float
```

**Fix:**
```bash
python fix_scores_final.py
```

**What it does:**
- Converts numeric values to typed objects: `0.75` → `{"@value": "0.75", "@type": "xsd:float"}`
- Targets ASFID keys: A, S, F, I_asfid, D
- Targets REVOI keys: R, E, V, O, I_revoi
- Targets other float properties: m0:epistemicGap, m0:mean

#### Step 1.2: Migrate to It/Im Keys
```bash
python migrate_firetriangle_to_it_im.py
```

**What it does:**
- **@context:** Renames `I_asfid` → `It`, `I_revoi` → `Im`
- **m0:asfidScores:** Renames key `I_asfid` → `It`
- **m0:revoiScores:** Renames key `I_revoi` → `Im`

**Before:**
```json
"m0:asfidScores": {
  "A": 0.75,
  "I_asfid": 0.80,
  ...
}
```

**After:**
```json
"m0:asfidScores": {
  "A": 0.75,
  "It": 0.80,
  ...
}
```

#### Step 1.3: Validate
```bash
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld instances/poclets/PocletName/M0_PocletName.jsonld
```

**Expected result:**
```
Conforms: True
```

---

### Phase 2: README Migration

#### Step 2.1: Run Migration Script
```bash
python migrate_readme_html_to_it_im.py
```

**What it does:**
- `|I⟩` → `|It⟩` in ASFID state vectors
- `|I⟩` → `|Im⟩` in REVOI state vectors
- `**I**` → `**It**` or `**Im**` in dimension tables
- `(A, S, F, I, D)` → `(A, S, F, It, D)` in dimension lists

#### Step 2.2: Manual Verification
Search for remaining ambiguous references:
```bash
grep -n "|I⟩\|**I**" M0_PocletName_README.md
```

**Should return:** No results (or only in quoted text/references)

#### Step 2.3: Visual Check
Open README and verify:
- [ ] State vectors use `|It⟩` (ASFID) and `|Im⟩` (REVOI)
- [ ] Dimension tables distinguish It vs Im
- [ ] No ambiguous `I` references remain

---

### Phase 3: HTML Simulation Migration

#### Step 3.1: Locate HTML File
HTML file location varies by poclet:
- `instances/poclets/PocletName/M0_PocletName.html` (root)
- `instances/poclets/PocletName/static/M0_PocletName.html` (subdirectory)

Update script path if needed:
```python
HTML_PATH = Path("E:/.../PocletName/static/M0_PocletName.html")
```

#### Step 3.2: Run Migration
```bash
python migrate_readme_html_to_it_im.py
```

**What it does:**
- `asfid: { ... I: 0.80 ... }` → `It: 0.80`
- `revoi: { ... I: 0.85 ... }` → `Im: 0.85`
- `${pole.asfid.I}` → `${pole.asfid.It}` in templates
- `${pole.revoi.I}` → `${pole.revoi.Im}` in templates

#### Step 3.3: Browser Test
1. Open HTML in browser
2. Check JavaScript console for errors
3. Verify ASFID/REVOI scores display correctly
4. Test interactive features

---

## ✅ Verification Checklist

### JSON-LD (`M0_PocletName.jsonld`)
- [ ] SHACL validation passes (`Conforms: True`)
- [ ] `@context` defines `It` and `Im` with `@type: xsd:float`
- [ ] `m0:asfidScores` uses key `It` (not `I` or `I_asfid`)
- [ ] `m0:revoiScores` uses key `Im` (not `I` or `I_revoi`)
- [ ] All score values are typed objects with `@type: xsd:float`
- [ ] `m0:epistemicGap` is typed as `xsd:float`

### README (`M0_PocletName_README.md`)
- [ ] ASFID state vectors use `|It⟩`
- [ ] REVOI state vectors use `|Im⟩`
- [ ] Dimension tables distinguish It (Information/Territory) vs Im (Interoperability/Map)
- [ ] No ambiguous `|I⟩` or `**I**` references remain
- [ ] Dimension lists show `(A, S, F, It, D)` and `(R, E, V, O, Im)`

### HTML Simulation (`M0_PocletName.html`)
- [ ] JavaScript objects use `It` key in `asfid`
- [ ] JavaScript objects use `Im` key in `revoi`
- [ ] Template strings reference `.asfid.It` and `.revoi.Im`
- [ ] CSS variables use `--col-It` and `--col-Im` (if applicable)
- [ ] No JavaScript console errors
- [ ] Scores display correctly in UI
- [ ] Interactive features work

---

## 🚨 Common Issues and Fixes

### Issue 1: SHACL Validation Fails with xsd:double
**Symptom:**
```
Value Node: Literal("0.75", datatype=xsd:double)
Expected: xsd:float
```

**Cause:** Numeric values in JSON are parsed as `xsd:double` by default

**Fix:** Use `fix_scores_final.py` to convert to typed float objects

---

### Issue 2: Script Doesn't Find Files
**Symptom:**
```
⚠ File not found: .../M0_PocletName.html
```

**Cause:** File is in a different location (e.g., `static/` subdirectory)

**Fix:** Update script path or move file to expected location

---

### Issue 3: README Has Multiple |I⟩ That Weren't Replaced
**Symptom:** Script reports only 1-2 modifications, but file has many `|I⟩`

**Cause:** 
- Regex pattern didn't match all vector formats
- Vectors may use different notation styles

**Fix:** Manual find-replace with context awareness:
1. Find all `|I⟩` occurrences
2. For each, check context (ASFID section → `|It⟩`, REVOI section → `|Im⟩`)
3. Replace manually

---

### Issue 4: HTML Simulation Broken After Migration
**Symptom:** JavaScript errors in console or scores don't display

**Possible causes:**
- Missed a property reference (check all `.I` references)
- CSS variable not updated
- Template string syntax broken

**Debug:**
1. Open browser DevTools console
2. Look for specific error messages
3. Search HTML for remaining `.I` references
4. Verify object structure matches expected keys

---

## 📊 Migration Statistics (FireTriangle Case Study)

### Files Modified: 3
- `M0_FireTriangle.jsonld`
- `M0_FireTriangle_README.md`
- `M0_FireTriangle.html` (in `static/` subdirectory)

### Modifications Count: 18 total
- **JSON-LD:** 4 modifications (2 in @context, 2 in score objects)
- **README:** 1+ modifications (dimension lists + state vectors)
- **HTML:** 7 modifications (JavaScript objects + templates)
- **Additional:** 6 float typing fixes (epistemicGap + 5 ASFID/REVOI scores)

### Validation: ✅ Success
- SHACL validation: `Conforms: True`
- No JavaScript errors
- All features functional

### Time Required: ~15 minutes
- Script execution: <1 minute
- Manual verification: ~5 minutes
- Testing: ~5 minutes
- Documentation: ~5 minutes

---

## 🔮 Future Poclets: Use Templates

To avoid this migration for new poclets, use the **v2 templates**:

### Templates with It/Im Built-in
- **`M0_CONTEXT_TEMPLATE_v2.json`** - @context with It/Im typed as xsd:float
- **`M0_POCLET_TEMPLATE_v2.jsonld`** - Complete poclet structure

**Key features:**
- ✅ Pre-configured It/Im nomenclature
- ✅ All float properties correctly typed
- ✅ SHACL-compliant out of the box
- ✅ Multi-domain support

**Usage:**
```bash
# Copy template
cp M0_POCLET_TEMPLATE_v2.jsonld instances/poclets/NewPoclet/M0_NewPoclet.jsonld

# Customize metadata and scores
# ...

# Validate
pyshacl -s ontology/M0_Instances_Schema.shacl.ttl -df json-ld instances/poclets/NewPoclet/M0_NewPoclet.jsonld
```

---

## 📚 Related Documentation

- **TSCG Smart Prompt** - Complete framework documentation
- **M0 Templates Usage Guide** - How to create new poclets
- **SHACL Schema Documentation** - Validation constraints
- **Bicephalous Architecture Guide** - Territory/Map theoretical foundation

---

## 🤝 Contributing

If you migrate additional poclets and encounter issues not covered here, please document them and contribute to this guide.

**Contact:** Echopraxium (GitHub: @Echopraxium)

---

## 📜 License

This migration guide is part of the TSCG framework.
- **Documentation:** CC BY 4.0
- **Scripts:** BSD 3-Clause

---

## 🎓 Acknowledgments

This migration was developed collaboratively between Michel (Echopraxium) and Claude AI (Anthropic), demonstrating the TSCG principle of human-AI synergy in framework evolution.

**Migration completed:** 2026-04-18  
**First poclet migrated:** FireTriangle (canonical reference)
