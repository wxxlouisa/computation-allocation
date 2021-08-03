from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import random
#from score_estimation import ScoreEstimation
from decision_module import DecisionModuleOnline

class Resquest(BaseHTTPRequestHandler):

    def if_drop(self, req_json, drop_rate):
        #score = estimator.predict(req_json)
        score = random.random()
        return int(decider.decide(score, drop_rate) or 0)

    def do_POST(self):
        print(self.headers)
        print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length']))
        print("--------------------接受client发送的数据----------------")
        res1 = req_datas.decode('utf-8')
        res = json.loads(res1)
        print(res)

        drop_rate = res['drop_rate']
        # create resp data
        data1 = {'drop':self.if_drop(res, drop_rate)}
        # encode python obj -> json obj
        data = json.dumps(data1)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

class ThreadingHTTPServer (ThreadingMixIn, HTTPServer):
    pass
if __name__ == '__main__':
    host = ('0.0.0.0', 2002)
    server = ThreadingHTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)

#    estimator = ScoreEstimation()
    decider = DecisionModuleOnline()
    server.serve_forever()
