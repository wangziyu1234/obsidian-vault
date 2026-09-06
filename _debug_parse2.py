#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

test_text = """# 1987年考研数学二试题

年全国硕士研究生招生考试试题
19874
（试卷Ⅲ）
一、填空题（本题共5 小题,每小题3分,满分15分)
（1）设= ln（1＋aα）,其中 α为非零常数,则=
（2）曲线 = arctan α 在横坐标为 1 的点处的切线方程是
;法线方程是
（3）积分中值定理的条件是
,结论是
n-2
lim
(4)
n→8
(5)|f'(x)dx =
f'(2x)dx =
二、（本题满分6分)
求极限lim
x-0
三、（本题满分7分)
dx
dx
y = 5(1 - cos t),
四、（本题满分8分)
计算定积分
xarcsin xdx.
五、（本题满分8分)
设 D 是由曲线= sin ＋1与三条直线 α =O,α = π,=O 围成的曲边梯形
"""

lines = test_text.split('\n')
q_pat_cn = re.compile(r'^[（(](\d+)[）)]')
q_pat_plain = re.compile(r'^(\d+)[.．]')
sec_pat = re.compile(r'^[一二三四五六七八九十]+[、．.]')

questions = []
current_section = ''
current_q = ''
current_qnum = ''

for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        if current_q:
            current_q += '\n'
        continue

    m_sec = sec_pat.match(stripped)
    m_cn = q_pat_cn.match(stripped)
    m_pl = q_pat_plain.match(stripped)

    print(f"Line {i}: {stripped[:50]}")
    print(f"  sec={bool(m_sec)} cn={bool(m_cn)} pl={bool(m_pl)}")

    if m_sec:
        if current_q and current_qnum:
            questions.append((current_section, current_qnum, current_q.strip()))
            print(f"  -> FLUSHED Q {current_qnum}")
            current_q = ''
            current_qnum = ''
        current_section = stripped.rstrip('：:')
        print(f"  -> SECTION: {current_section}")
        continue

    if m_cn:
        if current_q and current_qnum:
            questions.append((current_section, current_qnum, current_q.strip()))
            print(f"  -> FLUSHED Q {current_qnum}")
        current_qnum = m_cn.group(1)
        current_q = stripped + '\n'
        print(f"  -> NEW Q: {current_qnum}")
        continue

    if m_pl:
        if current_q and current_qnum:
            questions.append((current_section, current_qnum, current_q.strip()))
            print(f"  -> FLUSHED Q {current_qnum}")
        current_qnum = m_pl.group(1)
        current_q = stripped + '\n'
        print(f"  -> NEW Q: {current_qnum}")
        continue

    current_q += stripped + '\n'

if current_q and current_qnum:
    questions.append((current_section, current_qnum, current_q.strip()))
    print(f"  -> FLUSHED Q {current_qnum}")

print(f"\nTotal: {len(questions)} questions")
for sec, qnum, qtxt in questions:
    print(f"  [{sec}] Q{qnum}: {qtxt[:60]}...")
