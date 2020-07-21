import requests
import hjson
import urllib.parse
import json
import time


def _main():
    h = {
        "Cookie": "COOKIE_LOGIN_USER=edrive_view_mode=icon; apm_ct=20200415102651680; apm_uid=29FAD3AAF7227DFC8D69DE214255C5A8; apm_ip=117.152.46.9; apm_ua=F49C41BE171437757C72FF333488A319; _ga=GA1.2.597408328.1587037854; offline_Pic_Showed=true; wpsGuideStatus=true; shareId_136723510=null; shareId_105944752=null; shareId_104180915=null; shareId_1601806=null; shareId_161893853=null; shareId_162635301=null; UM_distinctid=171a13870dd82-03b9857e7e8cf4-70103e47-144000-171a13870de3f0; Hm_lvt_79fae2027f43ca31186e567c6c8fe33e=1587547763; svid=65A0409DA903536E5B0B0EE956E32855; s_fid=439CADEA903B92DB-07A116C92EFCEFD3; lvid=c1238943c866cbbe5ba947ef92efd77e; nvid=1; trkId=98E63362-4356-43AB-8496-517CCB879FF2; Login_Hash=; JSESSIONID=aaai9_nnLa3NShiLkFIgx; COOKIE_LOGIN_USER=8BD018E2B01D662A8DB930FABCFF8864EB3D685B79BDD63EB1652544332B9AFA8E371FCCCC14B0CC5D5F295A51E32C2F7E8115828F136B87B087CE29; validCodeTimestamp=0ac32825-f7ed-41d5-8142-938ee1f8b26e; shareId_168824830=ef8z; shareId_155057311=null; shareId_168824365=null  "
    }
    total = 1
    for pp in range(1,3):
        req = requests.get(
            'https://cloud.189.cn/v2/listPublicShare.action?userId=330783715&mediaType=0&orderBy=filename&order=ASC&pageNum=%s&pageSize=545' % pp
            , headers=h)
        j = hjson.loads(req.content.decode())
        for a in j['data']:
            print('%s/%s' % (total,1081))
            id = a["fileId"]
            name = str(a["fileName"])
            sid = a["shareId"]
            fo = a["isFolder"]
            t = [{"fileId": id, "fileName": name, "isFolder": 1 if fo else 0}]

            jdata = json.dumps(t, ensure_ascii=False).replace(' ','')

            data = ''
            data += 'type=SHARE_SAVE'
            data += '&taskInfos=' + str(urllib.parse.quote(jdata))
            data += '&targetFolderId=8146417517567840'
            data += '&shareId=' + str(sid)

            ih = h
            ih['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            resp = requests.post('https://cloud.189.cn/createBatchTask.action', headers=ih, data=data)
            print(name, resp.content.decode())
            total +=1
            time.sleep(0.5)


if __name__ == '__main__':
    _main()