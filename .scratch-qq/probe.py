import sqlite3, shutil, os
live = r"D:\ProgramData\tx\qq\Tencent Files\BA191806A3100767926833E1ACB004F4"
tmp = r"D:\obsidian\.scratch-qq"
for n in ["6A3F540F25B80B979F7FF97D89C23FEF","8D1A0ECED57102E56D6779DC8D8711D6","F002C85D8EB26803039C9F4F4B112DB8","FBCF9459F26148509F617A6899EA9732"]:
    src = os.path.join(live, n); dst = os.path.join(tmp, n + ".db")
    shutil.copyfile(src, dst)
    print("=====", n, os.path.getsize(src), "bytes")
    try:
        con = sqlite3.connect("file:%s?mode=ro" % dst.replace("\\","/"), uri=True)
        cur = con.cursor()
        rows = cur.execute("select type,name from sqlite_master limit 40").fetchall()
        print("   schema objects:", len(rows))
        for r in rows[:25]: print("     ", r)
        con.close()
    except Exception as e:
        print("   OPEN FAILED:", type(e).__name__, e)
