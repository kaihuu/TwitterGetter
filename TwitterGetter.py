import config, MongoDBAccessor
import json
from requests_oauthlib import OAuth1Session, OAuth1
import requests, sys, time
from datetime import datetime

ck = config.consumer_key
cs = config.consumer_secret
at = config.access_token
ats = config.access_token_secret

twitter = OAuth1Session(ck, cs, at, ats) 

url = 'https://api.twitter.com/1.1/search/tweets.json'

params = {'q' : '学生フォーミュラ', 'count': 100, 'result_type': 'recent', 'since_id':1042195085507457027}

res = twitter.get(url, params = params)



results = json.loads(res.text)

nRstTm = 15 * 3600 # Rate Limited待機時間

#for result in results['statuses']:
    #print(result)
    #print()

#print(results['search_metadata'])

#print(len(results['statuses']))


url2 = 'https://stream.twitter.com/1.1/statuses/filter.json'

auth = OAuth1(ck, cs, at, ats)


while(True):
    try:
        print('リクエスト')
        r = requests.post(url2, auth=auth, stream=True, data={"track":"学生フォーミュラ, #学生フォーミュラ"})
        if r.status_code == 200:
            print('コード')
            print(r)
            for line in r.iter_lines():
                print(json.loads(line.decode('utf-8')))
                print()
                MongoDBAccessor.InsertJSON(json.loads(line.decode('utf-8')))
        # 短時間でアクセスしすぎたら420エラーになるので待機
        elif r.status_code == 420:
            print('Rate Limited：',nRstTm,'分待機')
            time.sleep(nRstTm)
        else:
            # とりあえず処理抜けとく
            print('req.status_code',r.status_code)
            break
    
    except json.JSONDecodeError as e:
        print('再取得')
        print(datetime.now())
        pass
    
    except KeyboardInterrupt:
        print('処理終了')
        break
    
    except:
        print('except', sys.exc_info())
        pass