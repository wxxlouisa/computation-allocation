import http.client, urllib.parse
import json

# diag1 = {    'req_id':'111'
#              , 'drop_rate':0.8
#              , 'column_1':''
#              , 'column_2':''
#              , 'column_3':''
#              , 'column_4':''
#              , 'column_5':''
#              , 'column_6':''
#              , 'column_7':''
#              , 'column_8':''
#              , 'column_9':''
#              , 'column_10':''}
diag1 = {"req_id": "98c97f55-eb45-4d52-b068-c2f1a0d8fed6u1501",
         "drop_rate":0.5,
         "column_1": "1b41a7903979e216de70b53301f7a9c0",
          "column_2": "872ada276a69ae5d697f2e0d4bcf5c3e",
          "column_3": "6207f3b4a3142c333c502e017a05f504",
          "column_4": "54022593df8a87b4f4986dee6024183b",
          "column_5": "a6eaf58dfd869886465e0a0cf4b7ba62",
          "column_6": "98f674d60849b7871b2f1ef3ea6307b3",
          "column_7": "97e79c9ab772afa1cd5124d544931801",
          "column_8": "69d882255838835557dfe4c4cc3e4174",
          "column_9": "487140fbe07ced0bcc1500ca5bcf8baa",
          "column_10": "d50b6b95ef4d5913abd29e3d764f8391",
         "score":1.0,
          };
#要发送的数据 ，因为要转成json格式，所以是字典类型
data = json.dumps(diag1)

headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = http.client.HTTPConnection('localhost', 2002)
conn.request('POST', '/ippinte/api/scene/getall', data.encode('utf-8'), headers)#往server端发送数据
response = conn.getresponse()

stc1 = response.read().decode('utf-8')#接受server端返回的数据
stc = json.loads(stc1)

print("-----------------接受server端返回的数据----------------")
print(stc)
print("-----------------接受server端返回的数据----------------")

conn.close()
