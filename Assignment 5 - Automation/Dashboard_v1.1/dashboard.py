"""Loopback-only academic dashboard; no external dependencies."""
import json, re
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, unquote, quote
from pathlib import Path

PORT=8004
ROOT=Path(__file__).resolve().parent
SERVICES={'classification':8000,'alignment':8001,'priority':8002,'audit':8003}
MODEL_HASH='e7e440cacfc5926e4eab482bc9baad188eebedf2dbab22b21b3d49fcffac4239'

def upstream(port,path,method='GET',body=None):
    try:
        req=Request(f'http://127.0.0.1:{port}{path}',data=body,method=method,headers={'Content-Type':'application/json','Accept':'application/json'})
        with urlopen(req,timeout=90 if port==5678 else 10) as r:
            return r.status,json.load(r)
    except HTTPError as e:
        try: return e.code,json.load(e)
        except Exception: return e.code,{'message':'Upstream HTTP error'}
    except (OSError,ValueError):
        return 503,{'message':'Local service unavailable or response invalid. Check stored record before retrying.','production_authorized':False}

def health():
    out={}
    for name,port in SERVICES.items():
        code,b=upstream(port,'/health'); b=b if isinstance(b,dict) else {}
        version=b.get('model_version') if name=='classification' else b.get('engine_version',b.get('version'))
        expected={'classification':'NB-v1','alignment':'1.1.0','priority':'1.0.0','audit':'1.0.0'}[name]
        ok=code==200 and b.get('status')=='ok' and version==expected
        if name=='classification': ok=ok and b.get('model_loaded') is True and b.get('model_sha256')==MODEL_HASH
        out[name]={'port':port,'version':version,'expected':expected,'ok':ok}
    return out

class Handler(BaseHTTPRequestHandler):
    def send_data(self,status,data,kind='application/json; charset=utf-8'):
        raw=json.dumps(data,ensure_ascii=False).encode() if kind.startswith('application/json') else data
        self.send_response(status); self.send_header('Content-Type',kind); self.send_header('Content-Length',str(len(raw))); self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'"); self.end_headers(); self.wfile.write(raw)
    def allowed(self):
        return self.headers.get('Host') in ('localhost:8004','127.0.0.1:8004') and self.headers.get('Origin') in (None,'http://localhost:8004','http://127.0.0.1:8004') and self.headers.get('Sec-Fetch-Site') not in ('cross-site','same-site')
    def do_GET(self): self.route('GET')
    def do_POST(self): self.route('POST')
    def route(self,method):
        if not self.allowed(): return self.send_data(403,{'message':'Local origin required'})
        path=urlsplit(self.path).path
        if method=='GET' and path in ('/','/app.js','/style.css'):
            file,kind={'/':('index.html','text/html'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}[path]
            return self.send_data(200,(ROOT/file).read_bytes(),kind+'; charset=utf-8')
        if method=='GET' and path=='/api/health': return self.send_data(200,health())
        body=None
        if method=='POST':
            try:
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=50000 or self.headers.get_content_type()!='application/json': raise ValueError()
                body=self.rfile.read(n); obj=json.loads(body)
                if not isinstance(obj,dict): raise ValueError()
            except (ValueError,TypeError): return self.send_data(400,{'message':'Valid JSON object required'})
        if method=='POST' and path=='/api/submit':
            code,data=upstream(5678,'/webhook/it-work-triage-v31','POST',body)
            return self.send_data(code,data)
        if method=='GET' and path=='/api/items': return self.send_data(*upstream(8003,'/items'))
        m=re.fullmatch(r'/api/items/([^/]+)(/events|/review)?',path)
        if m:
            ident=unquote(m[1]); suffix=m[2] or ''
            if not ident or len(ident)>100 or '/' in ident or ident in ('.','..'): return self.send_data(400,{'message':'Invalid ID'})
            if (method=='GET' and suffix in ('','/events')) or (method=='POST' and suffix=='/review'):
                return self.send_data(*upstream(8003,'/items/'+quote(ident,safe='')+suffix,method,body))
        return self.send_data(404,{'message':'Not found'})

if __name__=='__main__':
    print('IT Work Triage dashboard: http://localhost:8004',flush=True)
    ThreadingHTTPServer(('127.0.0.1',PORT),Handler).serve_forever()
