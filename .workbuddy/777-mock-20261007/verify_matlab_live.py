from pathlib import Path
import os,re,json
base=Path('D:/obsidian/控制理论/青岛大学825真题/777改编模拟卷/Markdown笔记')
temp=Path(os.environ['TEMP'])/'qdu777_matlab_verify';temp.mkdir(exist_ok=True)
expect={
(1,3):('G','6*(p-1)/(p*(p+2)*(p+3)*(p+4))'),(1,4):('G','3/(p+1)'),(1,5):('G','K/(p*(p+3)*(p+5))'),(1,8):('Phi','18/(p^2+6*p+18)'),(1,12):('G','20/(p*(p+2)*(p+3))'),(1,14):('G','K/(p*(p+3)*(p+6))'),(1,15):('Gc','(1+a*T*p)/(1+T*p)'),(1,16):('P','1/(p+1)'),(1,17):('sys','1/p^2'),
(2,1):('G','k/(p*(p+a))'),(2,3):('G','1/(p+2)'),(2,4):('G','K*(p+1)/(p*(p+2)*(p+5))'),(2,8):('Phi','20/((p+10)*(p^2+2*p+2))'),(2,9):('G','2/(p+1)'),(2,13):('Gc','Kd*p+Kp+Ki/p'),(2,14):('G','K*(p+2)*(p+3)/(p*(p+1))'),(2,17):('sys','2*(p+5)/((p+2)*(p+3))'),
(3,1):('Phi','9*k1/(2*p^2+6*k2*p+9*k1-2)'),(3,4):('G','sqrt(2)*exp(-tau*p)/(p*(p+1))'),(3,8):('G','(2*p+3)/(p*(p+1)*(T*p+1))'),(3,10):('Gc','Kp+Kd*p'),(3,13):('G','k*(1-p)/(p*(p+2))'),(3,15):('G','k/(p*(p+1)*(p+2))'),(3,16):('Dc','K*(p-a)/(p-1)'),(3,17):('sys','(p+1)/(p*(p+2))'),
(4,1):('G','120/((p+1)*(p+2)*(p+3))'),(4,3):('Phi','18/(p^2+4*p+8)'),(4,6):('Gc','10*(10*p+1)/(100*p+1)'),(4,9):('G','K*(p+2)/(p*(p+1)*(p+3))'),(4,14):('G','k/(p*(p^2+4*p+8))'),(4,15):('G2','k2/(p*(T2*p+1))'),(4,16):('sys','[1/p,1/(p*(p+2))]'),(4,17):('G','2/((p+1)*(p+2))'),
(5,1):('G','K/(p*(p+2)*(p+4))'),(5,2):('G','2/(p+1)'),(5,3):('G','K/(p*(p+2)*(p+4))'),(5,4):('G','8/(p*(p+1)*(p+2))'),(5,5):('Gc','(1+a*T*p)/(1+T*p)'),(5,6):('G0','k/(p*(T*p+1))'),(5,8):('G','K*(p+4)/(p*(p+1)*(p+2))'),(5,14):('G','k/(p*(p+4)*(p+6))'),(5,15):('G','k/(p*(p+1)*(p+2))'),(5,16):('P','(p+2)/((p-1)*(p-1/2))'),(5,17):('sys','24/(p+2)')}
rows=[];functions=[]
for path in sorted(base.glob('*（试题）.md')):
 sid=int(path.name[:2]);text=path.read_text(encoding='utf8')
 for m in re.finditer(r'^## 第(\d+)题.*?\n([\s\S]*?)(?=^## |\Z)',text,re.M):
  num=int(m[1]);codes=re.findall(r'(?:```|~~~)matlab\n([\s\S]*?)(?:```|~~~)',m[2])
  for code in codes:
   index=len(rows)+1;code.encode('ascii')
   test=''
   if (sid,num) in expect:
    name,value=expect[sid,num];test=f'p=2+1i; actual=evalfr({name},p); expected={value}; assert(norm(actual-expected)<1e-9);'
   if (sid,num)==(3,16):test+=' assert(abs(Dc.Ts-1/2)<1e-12);'
   if (sid,num)==(5,16):test+=' assert(P.Ts==1);'
   if (sid,num)==(5,11):test+=' assert(r==1);'
   functions.append(f"case {index}\n{code}\n{test}\n")
   rows.append({'set':sid,'question':num,'transfer_checked':(sid,num) in expect})
matlab="""results=struct('index',{},'passed',{},'error',{});
for ix=1:COUNT
  try
    verify_block(ix);
    results(ix)=struct('index',ix,'passed',true,'error','');
  catch ex
    results(ix)=struct('index',ix,'passed',false,'error',ex.message);
  end
end
fid=fopen('OUTPUT','w');fprintf(fid,'%s',jsonencode(results));fclose(fid);
assert(all([results.passed]));
fprintf('MATLAB_BLOCKS_PASSED=%d\\n',numel(results));
function verify_block(ix)
K=2;k=2;a=3;b=0.2;c=0.3;Kp=2;Ki=3;Kd=0.5;T=0.4;Ts=0.5;k1=1.2;k2=0.8;T1=1;T2=0.5;tau=0.2;
switch ix
CASES
end
end
""".replace('COUNT',str(len(rows))).replace('OUTPUT',str(temp/'result.json').replace('\\','/')).replace('CASES','\n'.join(functions))
(temp/'verify_mock_codes.m').write_text(matlab,encoding='ascii')
(Path(__file__).parent/'matlab_runtime_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(temp/'verify_mock_codes.m')
