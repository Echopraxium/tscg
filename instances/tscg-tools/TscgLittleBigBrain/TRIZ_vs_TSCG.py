#!/usr/bin/env python3
"""
Comparaison de TRIZ (40 principes) vs TSCG (80 concepts M2)
en tant que systèmes de classification de problèmes techniques.
"""

import glob, os
print("Répertoire courant :", os.getcwd())
print("Recherche récursive de M0_*.jsonld :", glob.glob("**/M0_*.jsonld", recursive=True))
print("Recherche non récursive :", glob.glob("M0_*.jsonld"))

import json
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
from sentence_transformers import SentenceTransformer

# ---------------------------
# Configuration
# ---------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
TSCG_ROOT = SCRIPT_DIR.parent.parent.parent
ONTOLOGY_DIR = TSCG_ROOT / "ontology"
INSTANCES_DIR = TSCG_ROOT / "instances"

EXCLUDED_DIRS = {'_archives', '__pycache__', 'static', 'fixtures'}
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

TRIZ_ONTOLOGY = ONTOLOGY_DIR / "M1_extensions" / "systemic_modeling" / "M1_SystemicModeling.jsonld"
M2_ONTOLOGY = ONTOLOGY_DIR / "M2_GenericConcepts.jsonld"

print(f"Recherche de TRIZ ontology : {TRIZ_ONTOLOGY}")
print(f"Recherche de M2 ontology : {M2_ONTOLOGY}")

# ---------------------------
# 1. Extraction des principes TRIZ
# ---------------------------
def load_triz_principles():
    if not TRIZ_ONTOLOGY.exists():
        print(f"❌ Fichier introuvable : {TRIZ_ONTOLOGY}")
        return {}
    with open(TRIZ_ONTOLOGY, 'r', encoding='utf-8') as f:
        data = json.load(f)
    principles = {}
    for node in data.get('@graph', []):
        if 'm1:extension:systemic_modeling:principleNumber' in node:
            num = node['m1:extension:systemic_modeling:principleNumber']
            name = node.get('rdfs:label', '')
            code = node.get('m1:extension:systemic_modeling:code', '')
            principles[num] = {
                'name': name,
                'code': code,
                'description': node.get('rdfs:comment', '')
            }
    print(f"✅ Chargé {len(principles)} principes TRIZ.")
    return principles

# ---------------------------
# 2. Extraction des concepts M2
# ---------------------------
def load_tscg_concepts():
    if not M2_ONTOLOGY.exists():
        print(f"❌ Fichier introuvable : {M2_ONTOLOGY}")
        return {}
    with open(M2_ONTOLOGY, 'r', encoding='utf-8') as f:
        data = json.load(f)
    concepts = {}
    for node in data.get('@graph', []):
        if 'rdfs:label' in node and 'm2:hasStructuralGrammarFormula' in node:
            label = node['rdfs:label']
            concepts[label] = {
                'label': label,
                'description': node.get('rdfs:comment', '')
            }
    print(f"✅ Chargé {len(concepts)} concepts M2 TSCG.")
    return concepts

# ---------------------------
# 3. Extraction des exemples annotés
# ---------------------------
def load_annotated_examples(principles, concepts):
    if not INSTANCES_DIR.exists():
        print(f"❌ Dossier instances introuvable : {INSTANCES_DIR}")
        return []
    examples = []
    for fp in INSTANCES_DIR.rglob("*.jsonld"):
        if any(ex in fp.parts for ex in EXCLUDED_DIRS):
            continue
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            items = data.get('@graph', [data])
            for node in items:
                comment = node.get('rdfs:comment', '') or node.get('description', '') or node.get('dcterms:description', '')
                if not comment:
                    continue

                # Labels TRIZ
                triz_labels = set()
                applies = node.get('m1ext:appliesPrinciple') or node.get('appliesPrinciple') or node.get('m1:extension:systemic_modeling:appliesPrinciple')
                if applies:
                    iri = applies.get('@id', applies) if isinstance(applies, dict) else applies
                    if 'Principle_' in iri:
                        num_str = iri.split('Principle_')[-1].split('#')[0].split('/')[-1]
                        try:
                            num = int(num_str)
                            if num in principles:
                                triz_labels.add(principles[num]['code'])
                        except:
                            pass
                comment_lower = comment.lower()
                for num, p in principles.items():
                    if p['name'].lower() in comment_lower or p['code'].lower() in comment_lower:
                        triz_labels.add(p['code'])

                # Labels TSCG
                tscg_labels = set()
                mobilizes = node.get('m2:mobilizes', [])
                if isinstance(mobilizes, list):
                    for ref in mobilizes:
                        iri = ref.get('@id', ref) if isinstance(ref, dict) else ref
                        label = iri.split('#')[-1].split('/')[-1]
                        if label in concepts:
                            tscg_labels.add(label)
                for cname in concepts:
                    if cname.lower() in comment_lower:
                        tscg_labels.add(cname)

                if triz_labels or tscg_labels:
                    examples.append({
                        'text': comment,
                        'triz_labels': list(triz_labels),
                        'tscg_labels': list(tscg_labels),
                        'source': f"{fp.name}:{node.get('@id', '')}"
                    })
        except Exception:
            pass
    print(f"✅ Construit {len(examples)} exemples annotés.")
    return examples

# ---------------------------
# 4. Vectorisation
# ---------------------------
def vectorize_texts(texts, method='embedding'):
    if method == 'embedding':
        model = SentenceTransformer(EMBEDDING_MODEL)
        X = model.encode(texts, convert_to_numpy=True)
        print(f"   Embeddings dimension: {X.shape[1]}")
        return X
    else:
        vectorizer = TfidfVectorizer(max_features=1000)
        X = vectorizer.fit_transform(texts).toarray()
        print(f"   TF‑IDF dimension: {X.shape[1]}")
        return X

# ---------------------------
# 5. Évaluation robuste avec RandomForest
# ---------------------------
def evaluate_classifier(X, y, classifier_name):
    # Supprimer les colonnes avec moins de 2 exemples positifs
    col_sums = y.sum(axis=0)
    mask = col_sums >= 2
    y_filtered = y[:, mask]
    n_removed = y.shape[1] - y_filtered.shape[1]
    if n_removed > 0:
        print(f"   {n_removed} classes avec <2 exemples supprimées.")
    if y_filtered.shape[1] == 0:
        print("   Aucune classe avec ≥2 exemples.")
        return 0.0, 0.0, 0.0

    X_train, X_test, y_train, y_test = train_test_split(X, y_filtered, test_size=0.2, random_state=42)

    # Vérifier que dans le train chaque colonne a deux valeurs distinctes
    unique_counts = [len(np.unique(y_train[:, i])) for i in range(y_train.shape[1])]
    cols_to_keep = [i for i, uc in enumerate(unique_counts) if uc == 2]
    if len(cols_to_keep) < y_train.shape[1]:
        print(f"   {y_train.shape[1] - len(cols_to_keep)} colonnes constantes dans le train supprimées.")
        y_train = y_train[:, cols_to_keep]
        y_test = y_test[:, cols_to_keep]

    if y_train.shape[1] == 0:
        print("   Aucune classe valide restante après filtrage.")
        return 0.0, 0.0, 0.0

    # Utilisation de RandomForest avec class_weight='balanced'
    clf = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42))
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
    prec = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
    print(f"\n{classifier_name} - Macro average:")
    print(f"   Precision: {prec:.3f}")
    print(f"   Recall:    {rec:.3f}")
    print(f"   F1 score:  {f1:.3f}")
    return f1, prec, rec

def multilabel_binarize(labels_list, all_classes):
    class_to_idx = {c: i for i, c in enumerate(all_classes)}
    y = np.zeros((len(labels_list), len(all_classes)), dtype=np.int8)
    for i, lbls in enumerate(labels_list):
        for l in lbls:
            if l in class_to_idx:
                y[i, class_to_idx[l]] = 1
    return y

# ---------------------------
# 6. Main
# ---------------------------
def main():
    print("="*70)
    print("Comparaison TRIZ (40 principes) vs TSCG (80 concepts M2)")
    print("="*70)

    principles = load_triz_principles()
    concepts = load_tscg_concepts()
    if not principles or not concepts:
        print("Impossible de continuer sans les ontologies.")
        return

    examples = load_annotated_examples(principles, concepts)
    if not examples:
        print("Aucun exemple annoté trouvé. Vérifiez les fichiers M0.")
        return

    texts = [ex['text'] for ex in examples]

    triz_all_labels = list(set(lbl for ex in examples for lbl in ex['triz_labels']))
    tscg_all_labels = list(set(lbl for ex in examples for lbl in ex['tscg_labels']))

    print(f"\nNombre de classes TRIZ utilisées : {len(triz_all_labels)}")
    print(f"Nombre de classes TSCG utilisées : {len(tscg_all_labels)}")

    y_triz = multilabel_binarize([ex['triz_labels'] for ex in examples], triz_all_labels)
    y_tscg = multilabel_binarize([ex['tscg_labels'] for ex in examples], tscg_all_labels)

    method = 'embedding'
    X = vectorize_texts(texts, method=method)

    print("\n" + "="*70)
    print("Évaluation des classifieurs")
    print("="*70)

    print("\n--- TRIZ ---")
    f1_triz, prec_triz, rec_triz = evaluate_classifier(X, y_triz, "TRIZ (40 principes)")

    print("\n--- TSCG ---")
    f1_tscg, prec_tscg, rec_tscg = evaluate_classifier(X, y_tscg, "TSCG (80 concepts M2)")

    print("\n" + "="*70)
    print("Comparaison finale")
    print("="*70)
    print(f"TRIZ  - F1 = {f1_triz:.3f} | Precision = {prec_triz:.3f} | Recall = {rec_triz:.3f}")
    print(f"TSCG  - F1 = {f1_tscg:.3f} | Precision = {prec_tscg:.3f} | Recall = {rec_tscg:.3f}")

    if f1_tscg > f1_triz:
        print("\n✅ TSCG obtient un meilleur F1 que TRIZ.")
    elif f1_tscg < f1_triz:
        print("\n✅ TRIZ obtient un meilleur F1 que TSCG.")
    else:
        print("\n➖ Performance équivalente.")

    print("\nNote: Les résultats dépendent de la qualité et de la quantité des annotations.")

if __name__ == "__main__":
    main()