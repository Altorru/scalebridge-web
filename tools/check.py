#!/usr/bin/env python3
"""Check this standalone public web edition; no network or native build required."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlparse,unquote
import csv,io,json,hashlib,zipfile,sys
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key in ('href','src') and value:self.refs.append(value)
checked=0
for page in ROOT.glob('*.html'):
 parser=Links();parser.feed(page.read_text())
 for ref in parser.refs:
  url=urlparse(urljoin('http://local/'+page.name,ref))
  if url.hostname!='local':continue
  target=ROOT/unquote(url.path).lstrip('/')
  if url.path.endswith('/'):target=target/'index.html'
  assert target.is_file(),(page.name,ref);checked+=1
for file in (ROOT/'dist').glob('*.zip'):
 assert file.name in ['ScaleBridge-brand-kit.zip','ScaleBridge-demo-kit.zip']
 with zipfile.ZipFile(file) as z:
  assert z.testzip() is None
  manifest='FILES.json' if 'FILES.json' in z.namelist() else 'MANIFEST.json'
  rows=json.loads(z.read(manifest));assert set(z.namelist())=={r['path'] for r in rows}|{manifest}
  for r in rows:
   assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
   assert not r['path'].endswith(('.apk','.aab','.jar','.jks','.keystore','.pem','.p12'))
rows=list(csv.DictReader(io.StringIO((ROOT/'examples/demo/output.csv').read_text())))
export=json.loads((ROOT/'examples/demo/output.json').read_text())
assert len(rows)==len(export['measurements'])==3
assert export['schema_version']==1 and export['unit']=='kg'
assert export['measurements'][1]['body_fat_percent'] is None
for row,measurement in zip(rows,export['measurements']):
 assert row['date']==measurement['date'] and float(row['weight_kg'])==measurement['weight_kg']
assert (ROOT/'examples/demo/output.csv').read_bytes().count(b'\r\n')==4
files=[]
for path in sorted(ROOT.rglob('*')):
 if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or path.name=='PUBLIC_MANIFEST.json':continue
 assert not path.is_symlink()
 relative=path.relative_to(ROOT).as_posix();assert path.suffix not in ['.apk','.aab','.jar','.kt','.jks','.keystore','.pem','.p12','.woff','.woff2','.ttf']
 assert not relative.startswith(('evidence/','app/','pilot/private/'))
 files.append({'path':relative,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
manifest=ROOT/'PUBLIC_MANIFEST.json'
if '--write-manifest' in sys.argv:manifest.write_text(json.dumps(files,indent=2)+'\n')
else:assert json.loads(manifest.read_text())==files,'Inventory changed; review then regenerate manifest'
print(json.dumps({'local_references_checked':checked,'public_files':len(files),'zip_crc_and_hashes':'passed','fictional_csv_json':'passed','native_artifacts':'excluded'}))
