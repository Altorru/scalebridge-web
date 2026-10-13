#!/usr/bin/env python3
"""Rebuild only the two public web downloads using standard-library ZIP support."""
from pathlib import Path
import json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'dist';DEST.mkdir(exist_ok=True)
def pack(name,files,manifest_name):
 rows=[]
 with zipfile.ZipFile(DEST/name,'w',zipfile.ZIP_DEFLATED) as z:
  for arc,path in sorted(files.items()):
   data=path.read_bytes();info=zipfile.ZipInfo(arc,(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,data);rows.append({'path':arc,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
  info=zipfile.ZipInfo(manifest_name,(2026,10,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,json.dumps(rows,indent=2)+'\n')
 with zipfile.ZipFile(DEST/name) as z:assert z.testzip() is None
 return name
brand={p.relative_to(ROOT).as_posix():p for p in (ROOT/'assets').rglob('*') if p.is_file()}
brand.update({n:ROOT/n for n in ['BRAND.md','LICENSE','THIRD_PARTY.md','licenses/Lucide-ISC.txt']})
demo={n:ROOT/'examples/demo'/n for n in ['input-fr.csv','output.csv','output.json','result.json','START_HERE.txt','feedback.txt']};demo['LICENSE']=ROOT/'LICENSE'
print(pack('ScaleBridge-brand-kit.zip',brand,'MANIFEST.json'))
print(pack('ScaleBridge-demo-kit.zip',demo,'FILES.json'))
