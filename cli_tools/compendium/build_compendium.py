#!/usr/bin/env python3
"""build_compendium.py - READ-ONLY build of the TSCG Compendium static site.

Reads classification from HEAD (via annotate_compendium's convention rules, with
any in-file @tscg block winning) plus the m3:Audience facet on instances; derives
subjects + run-modes + titles; copies PLAYABLE sims into dist/ (junk excluded) and
repoints their "Play" link to the Pages-served path; injects the data into the
HTML template; writes dist/index.html.

It NEVER writes to source files - only to the output dir. This is the script the
GitHub Action runs. Companion (same folder): annotate_compendium.py, which owns
the classification rules (single source of truth).

Usage:  python build_compendium.py <repo_root> --template compendium_template.html --out dist
"""
import os, re, json, glob, shutil, argparse
import annotate_compendium as ann

CAT = {"poclets":"Poclet","tscg-tools":"TSCG Tool",
       "systemic-frameworks":"Systemic Framework","symbolic-system-grammars":"Symbolic System Grammar"}
DEF = {"poclets":["KitUser"],"tscg-tools":["KitCrafter","KitArchitect"],
       "systemic-frameworks":["KitCrafter","KitArchitect"],"symbolic-system-grammars":["KitCrafter","KitArchitect"]}

# dirs never copied into dist, and never a source of the canonical sim
COPY_IGNORE = shutil.ignore_patterns("node_modules","_archives","_proto*","previous",".git","*.zip")
SIM_EXCLUDE = ("/_archives/","/_proto","/node_modules/","/previous/","/ok/","/src/","/test/","_previous","_bak")

def read(p):
    try: return open(p,encoding="utf-8",errors="ignore").read()
    except Exception: return ""

def label_val(v):
    if isinstance(v,str): return v
    if isinstance(v,dict): return v.get("@value")
    if isinstance(v,list) and v: return label_val(v[0])
    return None

def inst_title(p):
    txt=read(p)
    m=re.search(r'"(?:m1|m1core):simulationTitle"\s*:\s*"([^"]+)"',txt)
    if m: return m.group(1)
    name=re.sub(r'^M0_|\.jsonld$','',os.path.basename(p)).lower()
    try: j=json.loads(txt)
    except Exception: j=None
    if j is not None:
        nodes=j.get("@graph",[j]) if isinstance(j,dict) else (j if isinstance(j,list) else [])
        for n in nodes:
            if isinstance(n,dict):
                nid=str(n.get("@id","")).split("#")[-1].split("/")[-1].lower()
                if (nid==name or nid.endswith(name)) and "rdfs:label" in n:
                    lv=label_val(n["rdfs:label"])
                    if lv: return lv
    m=re.search(r'"m0:name"\s*:\s*"([^"]+)"',txt)
    return m.group(1) if m else None

def md_h1(p):
    for i,l in enumerate(open(p,encoding="utf-8",errors="ignore")):
        if i>50: break
        m=re.match(r'#\s+(.+?)\s*#*\s*$',l.strip())
        if m: return m.group(1).strip()
    return None

def fname(p):
    b=re.sub(r'\.(md|py|js|html|yaml|yml|jsonld)$','',os.path.basename(p))
    return re.sub(r'^M0_','',b).replace('_',' ')

def section(kind, path):
    if kind in ("worksite","handover"): return "Project management"
    if kind=="epistemology": return "Epistemology"
    if kind in ("gate","tool","skill"): return "Gate tools & tooling"
    if kind=="layer" or (kind=="doc" and path.startswith("ontology/")): return "The M3–M0 layers"
    if kind in ("instance","poclet-asset","tool-asset","framework-asset","ssg-asset","simulation","simulation-src"): return None
    return "Guides & templates"

def find_sim(folder, name):
    """Pick the canonical standalone .html of an instance folder."""
    cands=[p.replace(os.sep,"/") for p in glob.glob(folder+"/**/*.html",recursive=True)]
    cands=[p for p in cands if not any(x in p.lower() for x in SIM_EXCLUDE)]
    if not cands: return None
    nl=name.lower()
    def score(p):
        pl=p.lower(); b=os.path.basename(pl)
        s=0
        if "/static/"+b==pl[pl.rfind("/static/"):] or "/_static/"+b==pl[pl.rfind("/_static/"):]: s+=4
        if "/static/" in pl or "/_static/" in pl: s+=2
        if b.startswith("m0_") and nl in b: s+=3
        elif nl in b: s+=1
        s-=pl.count("/")  # prefer shallower
        return s
    return sorted(cands,key=score,reverse=True)[0]

def build_subjects(root, outdir):
    subs=[]
    for cat in DEF:
        for d in sorted(glob.glob(os.path.join(root,"instances",cat,"*"))):
            if not os.path.isdir(d): continue
            models=sorted(set(glob.glob(d+"/**/M0_*.jsonld",recursive=True)+glob.glob(d+"/M0_*.jsonld")))
            if not models: continue
            name=os.path.basename(d)
            allf=[os.path.join(r,f) for r,_,fs in os.walk(d) for f in fs]
            htmls=[f for f in allf if f.lower().endswith(".html")]
            aud=sorted(set(re.findall(r"audience\.(Kit\w+)",read(models[0])))) or DEF[cat]
            has_local=(any(f.lower().endswith((".py",".bat")) for f in allf)
                       or (any(f.endswith("package.json") for f in allf) and any(f.endswith("main.js") for f in allf))
                       or any(f.endswith("requirements.txt") for f in allf))
            if htmls: mode="playable"            # browser-runnable; audience gates visibility, not deployment
            elif has_local: mode="local"         # needs install (script / Electron / build)
            else: mode="under-construction"
            rel=lambda x:os.path.relpath(x,root).replace(os.sep,"/")
            readme=next((f for f in allf if f.lower().endswith("_readme.md")),None)
            s={"name":name,"category":CAT[cat],"audience":aud,"mode":mode,
               "title":inst_title(models[0]) or fname(models[0]),
               "model":rel(models[0]),"sim":rel(htmls[0]) if htmls else None,
               "readme":rel(readme) if readme else None,"folder":rel(d),"files":len(allf)}
            if mode=="playable":
                canon=find_sim(d,name)
                if canon:
                    reldir=os.path.relpath(d,root).replace(os.sep,"/")   # instances/<cat>/<Name>
                    dst=os.path.join(outdir,reldir)
                    if os.path.exists(dst): shutil.rmtree(dst)
                    shutil.copytree(d,dst,ignore=COPY_IGNORE)
                    play=reldir+"/"+os.path.relpath(canon,d).replace(os.sep,"/")
                    if os.path.exists(os.path.join(outdir,play)):
                        s["play"]=play
            subs.append(s)
    return subs

def build_docs(root):
    docs=[]
    for full,rp in ann.rel_paths(root):
        kind,aud,status=ann.classify(rp)
        if kind in ("__OUT__","__UNCLASSIFIED__","instance"): continue
        sec=section(kind,rp)
        if not sec: continue
        title=(md_h1(full) if rp.endswith(".md") else None) or fname(rp)
        docs.append({"path":rp,"title":title,"kind":kind,
                     "audience":aud,"status":status,"section":sec})
    for p in glob.glob(os.path.join(root,"_02_housekeeping","**","*.md"),recursive=True):
        rp=os.path.relpath(p,root).replace(os.sep,"/")
        docs.append({"path":rp,"title":(md_h1(p) or fname(rp)),"kind":"housekeeping",
                     "audience":["KitArchitect"],"status":"draft","section":"Project management"})
    return docs

def run_gallery(root, outdir, script, site_url):
    import subprocess, shutil as sh
    if not os.path.exists(script):
        print(f"  [gallery] generator not found ({script}) - skipped"); return
    if sh.which("node") is None:
        print("  [gallery] node not available - skipped"); return
    out=os.path.join(outdir,"instances","simulation_gallery.html")
    os.makedirs(os.path.dirname(out),exist_ok=True)
    cmd=["node",script,"--root",root,"--output",out]+(["--site-url",site_url] if site_url else [])
    try:
        subprocess.run(cmd,check=True); print(f"  gallery: {out}")
    except Exception as e:
        print(f"  [gallery] failed: {e}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--template",default="compendium_template.html")
    ap.add_argument("--out",default="dist")
    ap.add_argument("--gallery-script",default="cli_tools/regenerate_simulation_gallery/generate_index.js")
    ap.add_argument("--site-url",default="")
    a=ap.parse_args()
    os.makedirs(a.out,exist_ok=True)
    subjects=build_subjects(a.root,a.out)
    docs=build_docs(a.root)
    data=json.dumps({"subjects":subjects,"docs":docs},ensure_ascii=False)
    html=read(a.template)
    if '"@@DATA@@"' not in html:
        raise SystemExit("template missing the \"@@DATA@@\" placeholder")
    open(os.path.join(a.out,"index.html"),"w",encoding="utf-8").write(html.replace('"@@DATA@@"',data))
    open(os.path.join(a.out,".nojekyll"),"w").close()
    gscript=a.gallery_script if os.path.isabs(a.gallery_script) else os.path.join(a.root,a.gallery_script)
    run_gallery(a.root,a.out,gscript,a.site_url)
    played=sum(1 for s in subjects if s.get("play"))
    print(f"built {a.out}/index.html")
    print(f"  subjects: {len(subjects)}  (playable copied & linked: {played})")
    print(f"  docs: {len(docs)}")

if __name__=="__main__": main()
