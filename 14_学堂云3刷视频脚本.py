import requests
from time import sleep
from multiprocessing import Pool
from pprint import pprint
import json
#脚本声明:每次使用前都需要去修改cookie值(有时间限制，每个cookie最多可以使用半天)

class course():
    header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'cookie': 'UM_distinctid=171957d590514c-05fb3675daf1cf-5313f6f-144000-171957d59063ba; access_token=gAAAAABevipiN6oXb1AZij91ChBFxBhKpxF71L08UsfBsaEJaOR43-nxHMrgAX-sJJrlSMt8ak7DLs5wFiFu4-HcuzkNGTAGbhILQOVcpXhoU4iaQ0VvNrY; xt=gAAAAABevipiSLN47SyIXeoBpROh4aDrrUssE1UKLhec_0BxAGkIt0IJke9C4F-zUKEKyXsesKkQwtP_lAP-b0ZsP7oT2SAcRuBKJpKlzeHgbEaJegHpnoQ; xt_expires_in=604800; identity=1',
            'Host': 'hncu.xuetangx.com',
            'If-Modified-Since': '0',
            'Referer': 'https://hncu.xuetangx.com/lms',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'xtbz': 'cloud',
            }
    length_dict = {}

    def get_length(self,cid):
        all_list = []
        done_list = []
        Not_done_list = []
        url = 'https://hncu.xuetangx.com/lms/api/v1/course/{}/courseware/'.format(cid)
        header = {'Accept': 'application/json, text/plain, */*',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                  'Cache-Control': 'no-cache',
                  'Connection': 'keep-alive',
                  'Content-Length': '20',
                  'Content-Type': 'application/json;charset=UTF-8',
                  'Cookie': 'UM_distinctid=171957d590514c-05fb3675daf1cf-5313f6f-144000-171957d59063ba; plat_id=231; org_id=392; mode=1; xt=gAAAAABevipiSLN47SyIXeoBpROh4aDrrUssE1UKLhec_0BxAGkIt0IJke9C4F-zUKEKyXsesKkQwtP_lAP-b0ZsP7oT2SAcRuBKJpKlzeHgbEaJegHpnoQ; xt_expires_in=604800; identity=1; access_token=gAAAAABevkfsuMQ34hKhtSoraxwKdSK1_u8EVp6unoVbZe3u35fc-wF8HKOx-XlZRmaFnQnEcJyhq34T_Jj3Ti_tqQNVkQabb2Lc5HfmvYyEtTBGPLZ-_VU; CNZZDATA1273255756=1907010495-1587345719-null%7C1589527334',
                  'Host': 'hncu.xuetangx.com',
                  'If-Modified-Since': '0',
                  'Origin': 'https://hncu.xuetangx.com',
                  'Referer': 'https://hncu.xuetangx.com/lms',
                  'Sec-Fetch-Dest': 'empty',
                  'Sec-Fetch-Mode': 'cors',
                  'Sec-Fetch-Site': 'same-origin',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                  'x-referer': 'https://hncu.xuetangx.com/lms#/video/24823/50157/9adb670e-8ac1-465c-8f6f-fb4661106d13/143451/0/videoDiscussion',
                  'X-Requested-With': 'XMLHttpRequest'}
        payload = {"class_id": "50157"}
        response = requests.post(url, data=json.dumps(payload), headers=header)
        response = response.json()
        list = response['data']
        for item in range(len(list)):
            all_list += list[item]['videosRecord']['all']
            done_list += list[item]['videosRecord']['done']
        for it in all_list:
            if it not in done_list:
                Not_done_list.append(it)
        return Not_done_list

    def view_media(self,page, length, cid):
        rate = 15  # 视频播放速率
        count = int(length / rate) + 1
        for it in range(1, count):
            getData = {'i': '5',
                       'et': 'heartbeat',
                       'p': 'web',
                       'n': 'cc',
                       'lob': 'cloud3',
                       'cp': it * rate,
                       'fp': '0',
                       'tp': '0',
                       'sp': '3',
                       'ts': '1589522708042',
                       'u': 951274,
                       'c': cid,
                       'v': page,
                       'cc': page,
                       'd': length,
                       'pg': '{}_qeuv'.format(page),
                       'sq': it,
                       't': 'video',
                       '_': '1589522708042', }
            response = requests.get("https://hncu.xuetangx.com/heartbeat", params=getData, headers=self.header)
            print(response.text)
        print('*' * 80)

    def start(self):
        cid = input("请输入你要刷的课程ID号:")
        self.list = self.get_length(cid)
        pool = Pool(7)
        for it in self.list:
            pool.apply_async(self.view_media, args=(it, 360, cid))
        pool.close()
        pool.join()


if __name__ == '__main__':
    brain = course()
    brain.start()
