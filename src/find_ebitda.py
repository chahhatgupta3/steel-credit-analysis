from pypdf import PdfReader
for path in ['docs/Integrated-Annual-Report-FY-2024-25.pdf', 'docs/fy25-integratedreport.pdf']:
    r = PdfReader(path)
    print('\n===', path)
    n = 0
    for i, p in enumerate(r.pages, 1):
        for line in (p.extract_text() or '').split('\n'):
            if 'ebitda' in line.lower() and any(c.isdigit() for c in line) and n < 25:
                print(i, '|', line.strip()[:110]); n += 1
