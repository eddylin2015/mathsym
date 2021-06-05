
import datetime
from email.message import Message
from http.server import BaseHTTPRequestHandler, HTTPServer 
from urllib import parse
TE_Storage = {}
class HandleRequests(BaseHTTPRequestHandler):
    def handle(self):
        try:
            BaseHTTPRequestHandler.handle(self)
        except Exception:
            print(Exception)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        TE={"St":"1+1","Val":2}
        SID=datetime.datetime.now().isoformat()
        TE_Storage[SID]=TE
        self.wfile.write(bytes( f"""
        <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
            <form method="post">
                <input type=hidden name="SID" value="{SID}">
                <table>
                   <tr><td style="vertical-align: top;">命題:
                       <td><div style="width:200x;height:100px;">
                           \\( \large {TE["St"]} \\)
                           </div>
                    <tr><td>答題:<td><input type=text name=Ans value=""><input type=submit value="提交">
                </table>
            </form>
        </body>
        </html>
        """, "utf-8") )       
        
    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        data=parse.parse_qs(post_body)
        SID=data[b"SID"][0].decode('utf-8')
        Ans=data[b"Ans"][0].decode('utf-8')
        TE=TE_Storage.get(SID)
        Message=""
        if TE==None :
            Message="超時!"
        else:
            Val=TE["Val"]
            Message=f"OK! 答案:{Val}"
        self.wfile.write(bytes(f'''{Message} <a href=/app> 下一題 </a>''', "utf-8") )   

    def do_PUT(self):
        self.do_POST()

HTTPServer(('127.0.0.1', 80), HandleRequests).serve_forever()