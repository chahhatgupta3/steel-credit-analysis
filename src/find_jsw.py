from pypdf import PdfReader
r = PdfReader('docs/fy25-integratedreport.pdf')
keys = ['consolidated balance sheet', 'consolidated statement of profit and loss', 'consolidated statement of cash flow']
for i, p in enumerate(r.pages, 1):
    t = ' '.join((p.extract_text() or '').lower().split())
    for k in keys:
        if k in t and i > 380:
            print(k, '-> page', i)
