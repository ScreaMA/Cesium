import json
import time
f=open('Carrier.czml','r',encoding='utf-8')
m=open('Carrier_change.czml','w+',encoding='utf-8')
str=json.loads(f.read())
str[0]['position']['cartographicDegrees'][2]=1000
for i in range(1,20):
    str[0]['position']['cartographicDegrees'][2] +=1000
    time.sleep(2)
    m.seek(0)
    m.write(json.dumps(str))
    print('running')
f.close()
m.close()