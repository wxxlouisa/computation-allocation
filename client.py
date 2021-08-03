import http.client, urllib.parse
import json

diag1 = {    'req_id':'111'
             , 'drop_rate':0.8
             , 'column_1':''
             , 'column_2':''
             , 'column_3':''
             , 'column_4':''
             , 'column_5':''
             , 'column_6':''
             , 'column_7':''
             , 'column_8':''
             , 'column_9':''
             , 'column_10':''}
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
