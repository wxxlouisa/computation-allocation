from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json
import random
import time
from score_estimation import ScoreEstimation
from decision_module import DecisionModuleOnline

class Resquest(BaseHTTPRequestHandler):

    def if_drop(self, req_json, drop_rate):
        req_json.pop('drop_rate')
        score = estimator.predict(req_json)
        return int(decider.decide(score, drop_rate))
    def explore_approach():
        data1 =
    def do_POST(self):
        r = random.random()
        if (r < 0.2):
            data1 =  explore_approach()
        else:
            req_datas = self.rfile.read(int(self.headers['content-length']))
            start = time.time()
            res1 = req_datas.decode('utf-8')
            res = json.loads(res1)
            drop_rate = res['drop_rate']
            # create resp data
            data1 = {'drop':self.if_drop(res, drop_rate)}
            # encode python obj -> json obj

        data = json.dumps(data1)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))
        end = time.time()
        print("time cost", str(end - start), "seconds")

class ThreadingHTTPServer (ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    host = ('0.0.0.0', 2002)
    server = HTTPServer(host, Resquest)
    print("Starting sever, listen at: %s:%s" % host)

    estimator = ScoreEstimation()
    decider = DecisionModuleOnline()
    server.serve_forever()
