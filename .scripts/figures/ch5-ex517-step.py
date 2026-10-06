# figure: 频域-例517-阶跃响应.png
import os
import runpy
from pathlib import Path
os.environ['CH5_EXAMPLE_OUTPUT']='\u9891\u57df-\u4f8b517-\u9636\u8dc3\u54cd\u5e94.png'
runpy.run_path(str(Path(__file__).with_name('ch5-bode-examples.py')),run_name='__main__')
