"""Verify the portable publication independently of the private workspace."""
from pathlib import Path
from zipfile import ZipFile
import json,hashlib,re
ROOT=Path(__file__).resolve().parent.parent
DOC=ROOT/'cs-2026/design-model'
files=json.loads((DOC/'files.json').read_text(encoding='utf-8'))
for item in files:
    p=DOC/item['path']
    assert p.is_file(),item['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],item['path']
for html in ROOT.rglob('*.html'):
    for href in re.findall(r'(?:href|src)="([^"]+)"',html.read_text(encoding='utf-8')):
        if href.startswith(('#','https:','http:')):continue
        assert (html.parent/href).exists(),href
models=list(DOC.glob('*.axmz'));assert len(models)==1
with ZipFile(models[0]) as z:
    assert 'sysml-model.auml' in z.namelist() and 'sysml-model.axmi' in z.namelist()
    text='\n'.join(z.read(n).decode('utf-8',errors='replace') for n in z.namelist())
    assert not re.search(r'(?<![A-Za-z])[A-Za-z]:[\\/]|Users[/\\]|PRIVATE KEY|ghp_[A-Za-z0-9]',text)
assert len(list((DOC/'images').glob('*.png')))==10
print('PASS: hashes, local links, native model, 10 PNGs, no workstation paths')
