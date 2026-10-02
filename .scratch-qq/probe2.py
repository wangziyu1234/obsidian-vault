import sqlite3, shutil, os, time, glob, hashlib, datetime
def stamp(): return datetime.datetime.now().strftime("%H:%M:%S")
live_db = r"D:\ProgramData\tx\qq\Tencent Files\2372025257\nt_qq\nt_db"
tmp = r"D:\obsidian\.scratch-qq\live"
os.makedirs(tmp, exist_ok=True)
print("=== live nt_db ?? ===")
names = sorted(os.listdir(live_db))
for n in names:
    p = os.path.join(live_db, n)
    if os.path.isfile(p): print("   %-34s %10d  %s" % (n, os.path.getsize(p), datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%m-%d %H:%M:%S")))
print("=== ?????? ===")
for n in ["nt_msg.db","profile_info.db","group_info.db","buddy_info.db","settings.db","misc.db"]:
    src = os.path.join(live_db, n)
    if not os.path.isfile(src): print("   %-20s (???)" % n); continue
    dst = os.path.join(tmp, n)
    try:
        shutil.copyfile(src, dst)
        con = sqlite3.connect("file:%s?mode=ro" % dst.replace("\\","/"), uri=True)
        cur = con.cursor()
        tabs = [r[0] for r in cur.execute("select name from sqlite_master where type='table'").fetchall()]
        print("   %-20s OK  ??=%d" % (n, len(tabs)))
        if n == "profile_info.db" or n == "nt_msg.db":
            print("        ?:", ", ".join(tabs[:40]))
            if n == "profile_info.db":
                for t in tabs:
                    if "profile" in t.lower() or "self" in t.lower() or "uid" in t.lower():
                        try:
                            cols = [d[1] for d in cur.execute("pragma table_info(%s)" % t).fetchall()]
                            print("        ", t, "cols:", cols)
                            rows = cur.execute("select * from %s limit 3" % t).fetchall()
                            for r in rows[:3]:
                                s = str(r)
                                print("          ", s[:300])
                        except Exception as e: print("          err", e)
        con.close()
    except Exception as e:
        print("   %-20s FAILED: %s %s" % (n, type(e).__name__, e))
