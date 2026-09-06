#!/usr/bin/env python3
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

test_lines = [
    "（1）设= ln（1＋aα）,其中 α为非零常数,则=",
    "（2）曲线 = arctan α 在横坐标为 1 的点处的切线方程是",
    "(4)",
    "(5)|f'(x)dx =",
    "1. 函数f(）=|-)(2)",
    "2.设函数y=f(α）由参数方程",
    "一、填空题（本题共5 小题,每小题3分,满分15分)",
    "二、（本题满分6分)",
]

q_pat_cn = re.compile(r'^[（(](\d+)[）)]')
q_pat_plain = re.compile(r'^(\d+)[.．]')
sec_pat = re.compile(r'^[一二三四五六七八九十]+[、．.]')

for line in test_lines:
    m_cn = q_pat_cn.match(line)
    m_pl = q_pat_plain.match(line)
    m_sec = sec_pat.match(line)
    print(f"  {repr(line[:40])}")
    print(f"    cn={bool(m_cn)} pl={bool(m_pl)} sec={bool(m_sec)}")
    if m_cn:
        print(f"    cn group1={m_cn.group(1)}")
    if m_pl:
        print(f"    pl group1={m_pl.group(1)}")
