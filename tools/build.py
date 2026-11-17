"""Reconstruit la liste des cartes (const DATA) d'index.html à partir de data/*.txt.
Une ligne = « français | anglais » ; « # id | Nom du thème » ouvre un thème.
Dans chaque thème, les cartes sont rangées de la plus fréquente à la moins fréquente."""
import glob, json, os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
themes, seen = [], set()
for f in sorted(glob.glob(os.path.join(root, 'data', '*.txt'))):
    for ln in open(f, encoding='utf-8'):
        ln = ln.strip()
        if not ln: continue
        if ln.startswith('#'):
            i, n = [x.strip() for x in ln[1:].split('|')]
            themes.append({'id': 'ph-' + i, 'nom': n, 'cards': []}); continue
        fr, en = [x.strip() for x in ln.split('|')]
        if fr.lower() in seen: continue          # doublon : on garde la première
        seen.add(fr.lower()); themes[-1]['cards'].append((fr, en))
for t in themes:   # fréquence 1 (premier tiers), 2, 3
    n = len(t['cards'])
    t['cards'] = [[fr, en, '', '', 1 + 3 * i // n] for i, (fr, en) in enumerate(t['cards'])]
p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
total = sum(len(t['cards']) for t in themes)
s = re.sub(r'const DATA = \[.*?\];\n', lambda m: 'const DATA = ' + json.dumps(themes, ensure_ascii=False, separators=(',', ':')) + ';\n', s, count=1, flags=re.S)
s = re.sub(r'(<p class="lead">L\'anglais de la pharmacie et de la santé : )[\d  ]+', lambda m: m.group(1) + f'{total:,}'.replace(',', ' '), s)
open(p, 'w', encoding='utf-8').write(s)
print(total, 'cartes,', len(themes), 'thèmes')
