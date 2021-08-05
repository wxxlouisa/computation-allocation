from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from multiprocessing import Process

import json
import random
import time
from score_estimation.score_estimation import ScoreEstimation
from score_estimation.lightgbm_regression import lgbm
from decision_module.decision_module import DecisionModuleOnline

class Resquest(BaseHTTPRequestHandler):
    def do_back_up(self, req_json, drop_rate):
        # return param: 0 or 1
        loc = req_json['column_1'] #string
        if (not loc in cnt_ratio_rec):
            return 1
        if (cnt_ratio_rec[loc] - eps <= drop_rate):
            return 1 # drop
        else:
            return 0 # do not drop

    def if_drop(self, req_json, drop_rate):
        if (req_json['need_back_up'] == 1):
             return self.do_back_up(req_json, drop_rate)

        req_json.pop('drop_rate')
        req_json.pop('need_back_up')
        req_json['score'] = 0.0
        score = estimator.predict(req_json)
        return int(decider.decide(score, drop_rate))

    def explore_approach(self):
         return {'drop':0} # do not drop

    def do_POST(self):
        r = random.random()
        start = time.time()
        if (r < 0.0001):
            data1 =  self.explore_approach()
        else:
            req_datas = self.rfile.read(int(self.headers['content-length']))
            res1 = req_datas.decode('utf-8')
            res = json.loads(res1)
            if (not 'need_back_up' in res):
                res['need_back_up'] = 0
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
#        print("time cost", str(end - start), "seconds")

if __name__ == '__main__':
    host = ('0.0.0.0', 2002)
    eps = 0.005
    server = HTTPServer(host, Resquest)
 #   print("Starting sever, listen at: %s:%s" % host)
    cnt_ratio_rec = json.load(open('./data/cnt_cusum_dict.json'))
#    estimator = ScoreEstimation()
    estimator = lgbm('/home/wangxuanxuan/computation-allocation/pred_gbm_model.txt')
    decider = DecisionModuleOnline('/home/wangxuanxuan/computation-allocation/pred_params.npy')
    server.serve_forever()
