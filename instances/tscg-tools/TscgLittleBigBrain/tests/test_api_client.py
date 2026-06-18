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
        try:
            data = self._fetch_from_api()
            if data:
                return data
        except Exception as e:
            print(f"⚠️  API query failed: {e}")

        if self.m0_dirs:
            poclets = self._load_from_files()
            if poclets:
                print(f"✅ Loaded {len(poclets)} poclets from automatic scan")
                return poclets

        print("⚠️  No local poclets found. Using hardcoded synthetic poclets.")
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

    def _extract_from_vector(self, node, prefix='asfid') -> Dict[str, float]:
        """
        Extrait les scores depuis les structures comme m0:asfidAnalysis ou m0:mapSpace.
        """
        result = {}
        if prefix == 'asfid':
            analysis = node.get('m0:asfidAnalysis', {})
            if analysis:
                state_vec = analysis.get('stateVector', [])
                dims = analysis.get('dimensions', ['A','S','F','I','D'])
                for i, dim in enumerate(dims):
                    if i < len(state_vec):
                        result[dim] = float(state_vec[i])
        else:  # revoi
            map_space = node.get('m0:mapSpace', {})
            revi_vec = map_space.get('reviStateVector', [])
            dims = map_space.get('dimensions', ['R','E','V','O','I'])
            for i, dim in enumerate(dims):
                if i < len(revi_vec):
                    result[dim] = float(revi_vec[i])
        return result

    def _load_from_files(self) -> List[Dict]:
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

                    # Fonction pour parcourir la racine et @graph
                    def process_node(node):
                        asfid = {}
                        revoi = {}
                        # 1. SHACL
                        asfid_obj = node.get('m0:asfidScores', {})
                        revoi_obj = node.get('m0:revoiScores', {})
                        for k, v in asfid_obj.items():
                            if k == 'm0:scoreA': asfid['A'] = self._extract_score(v)
                            elif k == 'm0:scoreS': asfid['S'] = self._extract_score(v)
                            elif k == 'm0:scoreF': asfid['F'] = self._extract_score(v)
                            elif k == 'm0:scoreIt': asfid['It'] = self._extract_score(v)
                            elif k == 'm0:scoreD': asfid['D'] = self._extract_score(v)
                        for k, v in revoi_obj.items():
                            if k == 'm0:scoreR': revoi['R'] = self._extract_score(v)
                            elif k == 'm0:scoreE': revoi['E'] = self._extract_score(v)
                            elif k == 'm0:scoreV': revoi['V'] = self._extract_score(v)
                            elif k == 'm0:scoreO': revoi['O'] = self._extract_score(v)
                            elif k == 'm0:scoreIm': revoi['Im'] = self._extract_score(v)
                        # 2. Ancien format m0:asfidAnalysis / m0:mapSpace
                        if not asfid:
                            asfid = self._extract_from_vector(node, 'asfid')
                        if not revoi:
                            revoi = self._extract_from_vector(node, 'revoi')
                        # 3. Clés directes (ancien)
                        if not asfid:
                            for d in ['A','S','F','It','D']:
                                if d in node:
                                    asfid[d] = self._extract_score(node[d])
                        if not revoi:
                            for d in ['R','E','V','O','Im']:
                                if d in node:
                                    revoi[d] = self._extract_score(node[d])
                        return asfid, revoi

                    all_asfid = {}
                    all_revoi = {}
                    a, r = process_node(data)
                    all_asfid.update(a)
                    all_revoi.update(r)
                    if '@graph' in data:
                        for node in data['@graph']:
                            a, r = process_node(node)
                            all_asfid.update(a)
                            all_revoi.update(r)

                    if not all_asfid and not all_revoi:
                        continue

                    scores = {
                        'A': all_asfid.get('A', 0.0),
                        'S': all_asfid.get('S', 0.0),
                        'F': all_asfid.get('F', 0.0),
                        'It': all_asfid.get('It', 0.0),
                        'D': all_asfid.get('D', 0.0),
                        'R': all_revoi.get('R', 0.0),
                        'E': all_revoi.get('E', 0.0),
                        'V': all_revoi.get('V', 0.0),
                        'O': all_revoi.get('O', 0.0),
                        'Im': all_revoi.get('Im', 0.0),
                    }

                    if any(v > 0.0 for v in scores.values()):
                        scored_files += 1
                        label = data.get('rdfs:label', filepath.stem)
                        scores['label'] = label
                        poclets.append(scores)
                except Exception as e:
                    # print(f"  Warning: {filepath.name}: {e}")
                    pass

        print(f"  Scanned {total_files} JSON-LD files, found {scored_files} with scores, kept {len(poclets)}")
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