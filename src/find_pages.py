import glob
from pypdf import PdfReader

RULES = {
    'BALANCE SHEET': ['consolidated', 'total assets', 'total equity'],
    'PROFIT & LOSS': ['consolidated', 'profit before', 'finance costs'],
    'CASH FLOW':     ['consolidated', 'operating activities', 'net cash'],
}

for path in sorted(glob.glob('docs/*.pdf')):
    reader = PdfReader(path)
    print(f'\n=== {path}  ({len(reader.pages)} pages)')
    hits = {k: [] for k in RULES}
    for i, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or '').lower()
        for name, words in RULES.items():
            if all(w in text for w in words):
                hits[name].append(i)
    for name, pages in hits.items():
        print(f'{name}: pages {pages[:12]}')
