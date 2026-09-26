# -*- coding: utf-8 -*-
"""渲染剩余 23 份讲义 PDF -> _pdf/<key>_pNNN.jpg（150dpi，可重跑）"""
import os
import glob

import fitz

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = ROOT
OUT = os.path.join(os.path.dirname(ROOT), "_pdf")

n_pages = 0
for pdf in sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf"))):
    key = os.path.splitext(os.path.basename(pdf))[0]
    doc = fitz.open(pdf)
    for i, page in enumerate(doc, 1):
        out = os.path.join(OUT, "%s_p%03d.jpg" % (key, i))
        if os.path.exists(out):
            continue
        pix = page.get_pixmap(dpi=150)
        pix.save(out)
        n_pages += 1
    print("%-8s %2d pages" % (key, doc.page_count))
    doc.close()
print("rendered new pages:", n_pages)
