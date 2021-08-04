import http.client, urllib.parse
import pandas as pd
import json


class TestDiag1:
    def send_drop_ratio(self, drop_ratio, diag1):
        diag1['drop_rate'] = drop_ratio
        diag1['need_back_up'] = 1
        drop_res = self.test_diag1(diag1)
        return drop_res['drop']

    def test_diag1(self, diag1):
        #要发送的数据,是字典类型
        data = json.dumps(diag1)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection('localhost', 2002)
        #往server端发送数据
        conn.request('POST', '/ippinte/api/scene/getall', data.encode('utf-8'), headers)
        response = conn.getresponse()

        stc1 = response.read().decode('utf-8')#接受server端返回的数据
        stc = json.loads(stc1)
 #       print("-----------------接受server端返回的数据----------------")
#        print(stc)
        return stc
  #      print("-----------------finish----------------")
        conn.close()

if __name__ == '__main__':

    obj = TestDiag1()
    total = 0
    sum = 0
    drop_cnt = 0
    data = pd.read_csv('./data/source.post.csv')
    my_rec = []
    batch_size = 500
    rate = 0.01

    for i in range(0, batch_size):
        if i % 100 == 0:
            print(i)
        diag1 = data.sample().T.iloc[:,0].to_dict()
        res = obj.send_drop_ratio(rate, diag1) # send dict
        if res == 1: # drop
            total = total + diag1['score']
            drop_cnt += 1
        sum = sum + diag1['score']
        my_rec.append(diag1['score'])

    my_drop_score_ratio = total / sum
    best_score_ratio = 0.0
    my_rec.sort()
    cnt = int(batch_size * rate)
    for i in range(0, cnt):
        best_score_ratio += my_rec[i]
    best_score_ratio = best_score_ratio / sum

    print(best_score_ratio, my_drop_score_ratio)
    print(drop_cnt / batch_size)
