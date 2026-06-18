import requests
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

class TscgAPIClient:
    def __init__(self, host: str = "localhost", port: int = 8000, timeout: int = 30,
                 m0_dir: str = None):
        self.base_url = f"http://{host}:{port}"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.m0_dirs = []
        if m0_dir:
            for d in m0_dir.split(';'):
                p = Path(d.strip())
                if p.exists():
                    self.m0_dirs.append(p)
        # Fallback : si aucun dossier n'a été fourni ou trouvé, utiliser le dossier instances par défaut
        if not self.m0_dirs:
            default_path = Path(r"E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances")
            if default_path.exists():
                self.m0_dirs.append(default_path)
                print(f"📁 Using default M0 instances directory: {default_path}")

    def is_running(self) -> bool:
        try:
            r = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            return r.status_code == 200
        except:
            return False

    def get_poclets_with_scores(self) -> List[Dict]:
        # 1) API
        try:
            data = self._fetch_from_api()
            if data:
                return data
        except Exception as e:
            print(f"⚠️  API query failed: {e}")

        # 2) Fichiers locaux (auto détection)
        if self.m0_dirs:
            poclets = self._load_from_files()
            if poclets:
                print(f"✅ Loaded {len(poclets)} poclets from local files")
                return poclets

        # 3) Synthétique
        print("⚠️  Using hardcoded synthetic poclets.")
        return self._get_hardcoded_poclets()

    def _fetch_from_api(self) -> List[Dict]:
        query = """
        PREFIX m0poclet: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?instance ?label ?A ?S ?F ?It ?D ?R ?E ?V ?O ?Im
        WHERE {
            ?instance m0poclet:scoreA ?A ;
                      m0poclet:scoreS ?S ;
                      m0poclet:scoreF ?F ;
                      m0poclet:scoreIt ?It ;
                      m0poclet:scoreD ?D ;
                      m0poclet:scoreR ?R ;
                      m0poclet:scoreE ?E ;
                      m0poclet:scoreV ?V ;
                      m0poclet:scoreO ?O ;
                      m0poclet:scoreIm ?Im .
            OPTIONAL { ?instance rdfs:label ?label }
        }
        LIMIT 100
        """
        response = self.session.post(
            f"{self.base_url}/corpus/sparql",
            json={"query": query, "format": "json"},
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            results = data.get("results", {})
            bindings = results.get("bindings", []) if isinstance(results, dict) else []
        else:
            bindings = []
        out = []
        for row in bindings:
            record = {}
            for k, v in row.items():
                if isinstance(v, dict):
                    record[k] = v.get("value", "")
                else:
                    record[k] = str(v)
            if any(record.get(k, '0') != '0' for k in ['A','S','F','It','D','R','E','V','O','Im']):
                out.append(record)
        return out

    def _extract_score(self, value) -> float:
        if value is None:
            return 0.0
        if isinstance(value, dict):
            if '@value' in value:
                try:
                    return float(value['@value'])
                except:
                    return 0.0
            return 0.0
        try:
            return float(value)
        except:
            return 0.0

    def _load_from_files(self) -> List[Dict]:
        # Exclure les dossiers d'archives et les copies 'static'
        excluded_dirs = {'_archives', '__pycache__', '.git', '.idea', 'venv', 'env', 'static'}
        poclets = []
        total_files = 0
        scored_files = 0

        for directory in self.m0_dirs:
            for filepath in directory.rglob("*.jsonld"):
                if any(part in excluded_dirs for part in filepath.parts):
                    continue
                total_files += 1
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Extraire les scores depuis la racine ou depuis chaque nœud du @graph
                    nodes_to_check = [data] + data.get('@graph', [])
                    asfid_obj = {}
                    revoi_obj = {}
                    for node in nodes_to_check:
                        if 'm0:asfidScores' in node:
                            asfid_obj.update(node['m0:asfidScores'])
                        if 'm0:revoiScores' in node:
                            revoi_obj.update(node['m0:revoiScores'])
                    # Fallback direct (ancien format)
                    if not asfid_obj:
                        asfid_obj = {k: data.get(f'm0:score{k.upper()}', None) for k in ['a','s','f','it','d']}
                    if not revoi_obj:
                        revoi_obj = {k: data.get(f'm0:score{k.upper()}', None) for k in ['r','e','v','o','im']}

                    scores = {
                        'A': self._extract_score(asfid_obj.get('A_score') or asfid_obj.get('A')),
                        'S': self._extract_score(asfid_obj.get('S_score') or asfid_obj.get('S')),
                        'F': self._extract_score(asfid_obj.get('F_score') or asfid_obj.get('F')),
                        'It': self._extract_score(asfid_obj.get('It_score') or asfid_obj.get('It')),
                        'D': self._extract_score(asfid_obj.get('D_score') or asfid_obj.get('D')),
                        'R': self._extract_score(revoi_obj.get('R_score') or revoi_obj.get('R')),
                        'E': self._extract_score(revoi_obj.get('E_score') or revoi_obj.get('E')),
                        'V': self._extract_score(revoi_obj.get('V_score') or revoi_obj.get('V')),
                        'O': self._extract_score(revoi_obj.get('O_score') or revoi_obj.get('O')),
                        'Im': self._extract_score(revoi_obj.get('Im_score') or revoi_obj.get('Im'))
                    }

                    if any(v > 0.0 for v in scores.values()):
                        scored_files += 1
                        # Utiliser le nom du fichier comme identifiant (pas de déduplication)
                        label = filepath.stem
                        scores['label'] = label
                        poclets.append(scores)
                except Exception as e:
                    pass  # silencieux pour éviter la pollution

        print(f"  Scanned {total_files} JSON-LD files, found {scored_files} with scores, kept {len(poclets)} files")
        return poclets

    def _get_hardcoded_poclets(self) -> List[Dict]:
        return [
            {"label": "FireTriangle", "A":0.75,"S":0.9,"F":0.6,"It":0.8,"D":0.5,
             "R":0.9,"E":0.7,"V":0.95,"O":0.8,"Im":0.9},
            {"label": "TrophicPyramid", "A":0.97,"S":0.92,"F":0.97,"It":0.9,"D":0.95,
             "R":0.85,"E":0.8,"V":0.85,"O":0.9,"Im":0.95},
            {"label": "NuclearReactor_PWR", "A":0.95,"S":0.9,"F":0.9,"It":0.85,"D":0.9,
             "R":0.95,"E":0.85,"V":0.9,"O":0.9,"Im":0.85},
            {"label": "NuclearReactor_FNR", "A":0.85,"S":0.9,"F":0.95,"It":0.8,"D":0.85,
             "R":0.9,"E":0.8,"V":0.85,"O":0.85,"Im":0.8},
            {"label": "TRIZ", "A":1.0,"S":1.0,"F":0.8,"It":1.0,"D":0.6,
             "R":1.0,"E":0.8,"V":1.0,"O":1.0,"Im":1.0},
            {"label": "RGB_Color", "A":0.6,"S":0.8,"F":0.5,"It":0.9,"D":0.4,
             "R":0.9,"E":0.5,"V":0.8,"O":0.8,"Im":0.7},
        ]

    def validate_poclet(self, poclet_data: Dict) -> Dict:
        try:
            r = self.session.post(
                f"{self.base_url}/corpus/validate",
                json=poclet_data,
                timeout=self.timeout
            )
            r.raise_for_status()
            return r.json()
        except Exception:
            asfid = poclet_data.get("asfid", {})
            revoi = poclet_data.get("revoi", {})
            a = [float(asfid.get(k, 0.0)) for k in ['A','S','F','It','D']]
            r = [float(revoi.get(k, 0.0)) for k in ['R','E','V','O','Im']]
            mean_a = np.mean(a)
            mean_r = np.mean(r)
            delta = abs(mean_a - mean_r) / np.sqrt(2)
            if delta < 0.05:
                cls = "Coherent"
            elif delta < 0.15:
                cls = "OnCriticalLine"
            elif delta < 0.30:
                cls = "Liminal"
            else:
                cls = "Enigmatic"
            return {"delta": delta, "spectral_class": cls}