from pathlib import Path
import re
from edit_recent import edit

stats=[]
def format_text(t):
    # Match the math papers' bold step labels; preserve H2 question anchors.
    t=re.sub(r'(?m)^####\s+((?:[（(]\d+[）)]|\d+[.、]).*)$',lambda m:'**'+m[1].replace('^*',r'^{\ast}')+'**',t)
    # A concise answer paragraph replaces an extra callout heading per question.
    t=re.sub(r'(?m)^> \[!tip\] 答案\n((?:>[^\n]*(?:\n|$))+)',lambda m:'**答案**\n\n'+re.sub(r'(?m)^> ?', '', m[1]).rstrip()+'\n',t)
    # Display blocks with several independent identities receive separate lines.
    def blocks(m):
        body=m[1]
        if r'\begin' in body or r'\left' in body or '>' in body:return m[0]
        chunks=re.split(r',?\s*\\qquad\s*',body.strip())
        if len(chunks)<2:return m[0]
        if not all('=' in s and s.count('{')==s.count('}') for s in chunks):return m[0]
        return '\n\n'.join('$$\n'+s.strip().rstrip(',')+'\n$$' for s in chunks)
    t=re.sub(r'(?m)^\$\$\n([\s\S]*?)^\$\$',blocks,t)
    t=re.sub(r'\n{4,}','\n\n\n',t)
    return t

for year in range(2006,2026):
    edit(year,'答案与解析',format_text)
print('Formatted answer steps and independent display identities for 20 years; question anchors retained.')
