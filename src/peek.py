from pypdf import PdfReader
r = PdfReader('docs/JSW Q4 FY25 consolidated filing.pdf')
print(len(r.pages), 'pages')
for i, p in enumerate(r.pages, 1):
    t = (p.extract_text() or '').strip().replace('\n', ' ')
    print(i, '|', t[:90])
