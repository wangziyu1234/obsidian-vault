from pathlib import Path
import subprocess
root=Path('D:/obsidian')
for name in ['现控强化3-20-ans-闭环结构图.png','现控强化3-24-ans-状态变量图.png']:
    data=subprocess.check_output(['git','show','HEAD:附件/'+name],cwd=root)
    (root/'附件'/name).write_bytes(data)
print('Restored two original figures from HEAD; corrected versions use new names.')
