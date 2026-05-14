# TSCG Ontology Validation Prerequisites

**Purpose:** Install Java JRE and Owlready2 for OWL reasoning and ontology validation  
**Target:** TSCG project contributors and developers  
**Updated:** 2026-05-13

---

## Overview

The TSCG ontology validation pipeline requires:
1. **Java JRE** (Java Runtime Environment) - for OWL reasoners
2. **Owlready2** - Python library with integrated OWL reasoning
3. **Python 3.8+** - assumed already installed

---

## Table of Contents

- [Java JRE Installation](#java-jre-installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Owlready2 Installation](#owlready2-installation)
- [Verification Tests](#verification-tests)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Java JRE Installation

### Why Java?

OWL reasoners (Pellet, HermiT) are Java-based. Owlready2 uses them as backend engines for logical consistency checking.

### Recommended: Eclipse Temurin (OpenJDK)

**Free, open-source, well-maintained**

---

### Windows

#### Method 1: Graphical Installer (Recommended)

**1. Download:**
- Visit: https://adoptium.net/
- Click **"Download"**
- Select:
  - **Version**: JRE 17 (LTS) or JRE 21 (LTS)
  - **OS**: Windows
  - **Architecture**: x64

**2. Install:**
```
1. Double-click the downloaded .msi file
2. Follow the installer wizard:
   ✅ Check "Set JAVA_HOME variable"
   ✅ Check "Add to PATH"
3. Click "Install"
4. Restart terminal/PowerShell
```

**3. Configure JAVA_HOME (if not set by installer):**

```powershell
# PowerShell as Administrator
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot" /M
```

**Important:** Replace `17.x.x` with your actual version number.

**4. Verify:**

```cmd
# Check JAVA_HOME
echo %JAVA_HOME%

# Check Java version (use quotes for paths with spaces)
"%JAVA_HOME%\bin\java" -version

# Or simply (if PATH is configured)
java -version
```

**Expected output:**
```
openjdk version "17.0.x" 2024-xx-xx
OpenJDK Runtime Environment Temurin-17.0.x+x
```

#### Method 2: Command Line (winget)

**Windows 10/11 with winget:**

```powershell
# PowerShell as Administrator
winget install EclipseAdoptium.Temurin.17.JRE
```

#### Method 3: Chocolatey

```powershell
# PowerShell as Administrator
choco install temurin17jre
```

---

### macOS

#### Method 1: Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Java JRE
brew install --cask temurin17
```

#### Method 2: Direct Download

- Visit: https://adoptium.net/
- Download macOS .pkg installer
- Double-click and follow installer

**Verify:**
```bash
java -version
echo $JAVA_HOME
```

**Set JAVA_HOME if needed:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH=$JAVA_HOME/bin:$PATH
```

---

### Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install OpenJDK JRE
sudo apt install openjdk-17-jre

# Verify
java -version
```

#### Fedora/RHEL

```bash
sudo dnf install java-17-openjdk
```

#### Arch Linux

```bash
sudo pacman -S jre-openjdk
```

**Set JAVA_HOME:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```

---

## Owlready2 Installation

**After Java is installed and verified:**

### Install via pip

```bash
# Standard installation
pip install owlready2

# Or with --break-system-packages if needed (Debian/Ubuntu)
pip install owlready2 --break-system-packages
```

### Verify Installation

```bash
python -c "from owlready2 import *; print('✅ Owlready2 ready!')"
```

**Expected output:**
```
✅ Owlready2 ready!
```

---

## Verification Tests

### Test 1: Java Installation

```bash
# Check Java version
java -version

# Expected: OpenJDK 17.x or higher
```

### Test 2: JAVA_HOME Configuration

**Windows:**
```cmd
echo %JAVA_HOME%
# Expected: C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot
```

**macOS/Linux:**
```bash
echo $JAVA_HOME
# Expected: /usr/lib/jvm/java-17-openjdk (or similar)
```

### Test 3: Owlready2 Import

```python
from owlready2 import *
print("✅ Owlready2 imported successfully")
```

### Test 4: Load and Reason on TSCG Ontology

**Create test script: `test_reasoning.py`**

```python
from owlready2 import *

print("=" * 70)
print("TSCG Ontology Reasoning Test")
print("=" * 70)

try:
    # Load ontology (adjust path to your TSCG repo)
    print("\n📂 Loading ontology...")
    onto = get_ontology("ontology/M2_GenericConcepts.jsonld").load()
    
    print(f"✅ Loaded: {onto.name}")
    print(f"   Classes: {len(list(onto.classes()))}")
    print(f"   Properties: {len(list(onto.properties()))}")
    
    # Run reasoner
    print("\n🔍 Running OWL reasoner (Pellet)...")
    with onto:
        sync_reasoner_pellet(infer_property_values=True)
    
    print("✅ Reasoning completed")
    
    # Check for inconsistencies
    print("\n🧪 Checking for inconsistencies...")
    inconsistent = list(onto.inconsistent_classes())
    
    if inconsistent:
        print(f"❌ Found {len(inconsistent)} inconsistent classes:")
        for cls in inconsistent:
            print(f"   - {cls.name}")
    else:
        print("✅ Ontology is logically consistent!")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED")
    print("=" * 70)
    
except FileNotFoundError as e:
    print(f"❌ Error: Ontology file not found")
    print(f"   Make sure you're in the TSCG repository root")
    print(f"   Error: {e}")
    
except Exception as e:
    print(f"❌ Error during reasoning: {e}")
    print(f"   Check Java installation and JAVA_HOME")

```

**Run the test:**

```bash
# From TSCG repository root
python test_reasoning.py
```

**Expected output:**
```
======================================================================
TSCG Ontology Reasoning Test
======================================================================

📂 Loading ontology...
✅ Loaded: M2_GenericConcepts
   Classes: 108
   Properties: 26

🔍 Running OWL reasoner (Pellet)...
✅ Reasoning completed

🧪 Checking for inconsistencies...
✅ Ontology is logically consistent!

======================================================================
✅ ALL TESTS PASSED
======================================================================
```

---

## Troubleshooting

### Issue 1: "java not recognized"

**Windows:**
```cmd
# Check if java.exe exists
where java

# If not found, reinstall Java with "Add to PATH" checked
# Or manually add to PATH (see Windows installation section)
```

**macOS/Linux:**
```bash
which java

# If not found:
export PATH=/usr/lib/jvm/java-17-openjdk/bin:$PATH
```

### Issue 2: "JAVA_HOME not set"

**Windows:**
```powershell
# Set system-wide (PowerShell as Admin)
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot" /M

# Then restart terminal
```

**macOS:**
```bash
# Add to ~/.zshrc
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```

**Linux:**
```bash
# Add to ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
```

### Issue 3: "ModuleNotFoundError: No module named 'owlready2'"

```bash
# Reinstall with verbose output
pip install --upgrade owlready2 -v

# Or try with user flag
pip install --user owlready2
```

### Issue 4: Owlready2 imports but reasoning fails

**Check Java is accessible from Python:**

```python
import subprocess
result = subprocess.run(['java', '-version'], capture_output=True)
print(result.stderr.decode())
```

**If this fails, Python can't find Java. Ensure:**
- Java is in PATH
- JAVA_HOME is set
- Terminal was restarted after Java installation

### Issue 5: "jpype" errors

```bash
# Owlready2 uses JPype to bridge Python-Java
# If issues occur, try reinstalling:
pip uninstall jpype1
pip install jpype1
pip install owlready2 --force-reinstall
```

---

## Next Steps

### 1. Integrate Reasoning into Linter

Update `cli-tools/ontology-linter/ontology_linter.py` to include OWL reasoning as Phase 3.5.

### 2. Validate All TSCG Ontologies

```bash
# Run linter with reasoning on all ontologies
python cli-tools/ontology-linter/ontology_linter.py ontology/ --strict
```

### 3. Add to CI/CD Pipeline

```yaml
# .github/workflows/validate-ontologies.yml
- name: Install Prerequisites
  run: |
    sudo apt-get install openjdk-17-jre
    pip install owlready2
    
- name: Validate Ontologies
  run: |
    python cli-tools/ontology-linter/ontology_linter.py ontology/ --strict
```

### 4. Use TSCG Ontology Diagnosis Pipeline

Follow the `tscg-ontology-diagnosis-pipeline` skill workflow for systematic validation with Human, LLM, and Formal Tools collaboration.

---

## Additional Resources

### Java
- **Eclipse Temurin (Adoptium)**: https://adoptium.net/
- **Oracle JDK**: https://www.oracle.com/java/technologies/downloads/
- **Amazon Corretto**: https://aws.amazon.com/corretto/

### Owlready2
- **Documentation**: https://owlready2.readthedocs.io/
- **GitHub**: https://github.com/pwin/owlready2
- **PyPI**: https://pypi.org/project/Owlready2/

### OWL Reasoners
- **Pellet**: https://github.com/stardog-union/pellet
- **HermiT**: http://www.hermit-reasoner.com/
- **ELK**: https://github.com/liveontologies/elk-reasoner

---

## Summary Checklist

After following this guide, you should have:

- [x] Java JRE 17+ installed
- [x] JAVA_HOME environment variable set
- [x] Java accessible in PATH
- [x] Owlready2 installed via pip
- [x] Verification tests passed
- [x] Able to load TSCG ontologies
- [x] Able to run OWL reasoning

**If all checkboxes are ticked: ✅ You're ready for TSCG ontology validation!**

---

**Questions or issues?** Open an issue on the TSCG GitHub repository.

**Last updated:** 2026-05-13  
**Version:** 1.0.0  
**Maintainer:** Echopraxium with Claude AI collaboration
