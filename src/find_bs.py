import glob
from pypdf import PdfReader
for path in sorted(glob.glob('docs/*.pdf')):
    reader = PdfReader(path)
    hits = []
    for i, page in enumerate(reader.pages, 1):
        t = (page.extract_text() or '').lower()
        if 'consolidated' in t and 'total assets' in t:
            hits.append(i)
        elif 'consolidated' in t and 'balance sheet' in t and 'borrowings' in t:
            hits.append(i)
    print(path, hits[:12])
