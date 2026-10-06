# figure: 频域-例57-实测幅频辨识.png
import os
import runpy
from pathlib import Path
os.environ['CH5_EXAMPLE_OUTPUT']='\u9891\u57df-\u4f8b57-\u5b9e\u6d4b\u5e45\u9891\u8fa8\u8bc6.png'
runpy.run_path(str(Path(__file__).with_name('ch5-bode-examples.py')),run_name='__main__')
