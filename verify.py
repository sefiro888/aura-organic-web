from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json,re

ROOT=Path(__file__).parent/'dist'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.assets=[];self.h1=0;self.images=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ['img','script'] and a.get('src'):self.assets.append(a['src'])
  if tag=='link' and a.get('href'):self.assets.append(a['href'])
  if tag=='h1':self.h1+=1
  if tag=='img':self.images.append(a)

files={f.name:Page(f.read_text(encoding='utf8')) for f in ROOT.glob('*.html')}
errors=[];links=0;images=0
for name,p in files.items():
 if p.h1!=1:errors.append(f'{name}: {p.h1} h1')
 if len(p.ids)!=len(set(p.ids)):errors.append(f'{name}: duplicate IDs')
 for a in p.images:
  images+=1
  if not a.get('alt'):errors.append(f'{name}: image without alt')
 for asset in p.assets:
  if not urlsplit(asset).scheme and not (ROOT/unquote(asset)).is_file():errors.append(f'{name}: missing asset {asset}')
 for href in p.links:
  links+=1;u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=u.path or name
  if target.endswith('.html') and target not in files:errors.append(f'{name}: missing page {target}')
  if u.fragment and target in files and unquote(u.fragment) not in files[target].ids:errors.append(f'{name}: missing anchor {href}')
for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',(ROOT/'assets/site.css').read_text(encoding='utf8')):
 if not url.startswith('data:') and not (ROOT/'assets'/url).is_file():errors.append(f'Missing CSS asset {url}')
result={'pages':len(files),'internal_and_external_links':links,'image_references':images,'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
