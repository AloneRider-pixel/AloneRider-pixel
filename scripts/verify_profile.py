import re
from pathlib import Path

text = Path('README.md').read_text(encoding='utf-8')
required = ['Selected projects', 'Evidence-first profile policy', 'StockSense AI', 'Aegis', 'Cloud Data Platform', 'ForgeAI', 'Event-Driven Platform']
missing = [section for section in required if section not in text]
if missing:
    raise SystemExit('Profile validation failed: ' + ', '.join(missing))
urls = re.findall(r'https?://[^) >]+', text)
if len(urls) < 10:
    raise SystemExit(f'Profile validation failed: expected >=10 project/profile links, found {len(urls)}')
print(f'profile verification passed: {len(urls)} links and {len(required)} required sections')