from pathlib import Path
import os,json,datetime
ROOT=Path(os.environ.get('PISA_RUN_ROOT',str(Path(__file__).resolve().parents[2]/'.reproduction/outputs'))).resolve()
def load_json(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def save_json(path,value):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def log(event,result,decision,problem='Ninguno'):
    with (ROOT/'RESEARCH_LOG.md').open('a',encoding='utf-8') as f:
        f.write(f'\n## {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n- Analysis: {event}\n- Result: {result}\n- Decision: {decision}\n- Problems: {problem}\n')
