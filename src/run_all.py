import subprocess, sys
year = sys.argv[1:]
for s in ['build_db', 'checks', 'stress']:
    print(f'\n=== {s}')
    subprocess.run([sys.executable, f'src/{s}.py', *year], check=True)
print('\n=== pytest')
subprocess.run([sys.executable, '-m', 'pytest', '-q'])
