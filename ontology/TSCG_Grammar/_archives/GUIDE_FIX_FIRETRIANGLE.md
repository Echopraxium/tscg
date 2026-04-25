# Correction du Typage Float pour M0_FireTriangle.jsonld

**Auteur:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-04-18

## Problème

La validation SHACL échoue sur `M0_FireTriangle.jsonld` car tous les scores sont typés `xsd:double` au lieu de `xsd:float`.

## Solution - Deux Options

### Option 1 : Modification Manuelle (Recommandée si tu veux voir le détail)

1. Ouvre `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\poclets\FireTriangle\M0_FireTriangle.jsonld`

2. Dans le bloc `"@context"`, ajoute le namespace `xsd` s'il n'existe pas déjà :
   ```json
   "xsd": "http://www.w3.org/2001/XMLSchema#"
   ```

3. Pour chaque propriété de score, remplace la définition simple par une définition typée :

   **AVANT :**
   ```json
   "m0:epistemicGap": "M0_Poclet#epistemicGap"
   ```

   **APRÈS :**
   ```json
   "m0:epistemicGap": {
     "@id": "M0_Poclet#epistemicGap",
     "@type": "xsd:float"
   }
   ```

4. Propriétés à modifier (12 au total) :
   - `m0:epistemicGap`
   - `m0:mean`
   - `eagle_eye:Attractor`
   - `eagle_eye:Structure`
   - `eagle_eye:Flow`
   - `eagle_eye:Information`
   - `eagle_eye:Dynamics`
   - `sphinx_eye:Representable`
   - `sphinx_eye:Evolvable`
   - `sphinx_eye:Verifiable`
   - `sphinx_eye:Observable`
   - `sphinx_eye:Interoperable`

5. **Fichier de référence complet:** `M0_FireTriangle_CONTEXT_CORRECTED.json` contient le `@context` complet corrigé que tu peux copier-coller.

### Option 2 : Script Python Automatique (Plus Rapide)

1. Copie `fix_firetriangle_float.py` dans la racine de ton dépôt :
   ```
   E:\_00_Michel\_00_Lab\_00_GitHub\tscg\fix_firetriangle_float.py
   ```

2. Exécute le script :
   ```bash
   cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg
   python fix_firetriangle_float.py
   ```

3. Le script va :
   - Lire M0_FireTriangle.jsonld
   - Ajouter les définitions `@type: xsd:float` dans le @context
   - Sauvegarder le fichier modifié (UTF-8, ensure_ascii=False)

## Vérification

Après la correction, relance la validation SHACL :

```bash
cd E:\_00_Michel\_00_Lab\_00_GitHub\tscg

pyshacl -s ontology/M0_Instances_Schema.shacl.ttl ^
        -df json-ld ^
        instances/poclets/FireTriangle/M0_FireTriangle.jsonld
```

Tu devrais obtenir `Conforms: True` !

## Pour les Futurs Poclets

Quand tu crées de nouveaux poclets M0, **pense à inclure ces définitions typées dans le @context dès le départ** pour éviter ce problème.

Tu peux utiliser `M0_FireTriangle_CONTEXT_CORRECTED.json` comme template de référence.
