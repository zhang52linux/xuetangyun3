import requests
from urllib.parse import unquote
from pprint import pprint
import ssl
import json
import re

class xuetangyun_videp():
    class_list = {}
    term_id = 0
    term_list = {'1':965,'2':1423}
    def showTheme(self):
        print('************************************************************************')
        print('*****                       1、2020春                                ***')
        print('*****                       2、2020春学校公选课                      ***')
        print('************************************************************************')

    def get_class(self,term):
        header = {  'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Cookie': 'UM_distinctid=171957d590514c-05fb3675daf1cf-5313f6f-144000-171957d59063ba; plat_id=231; org_id=392; mode=1; CNZZDATA1273255756=1907010495-1587345719-null%7C1592129746; access_token=gAAAAABe5gHg9caBHJ5pHkbz47pFzLbp-tY9NBJ9wwuXGpqCv1drO7VSAOGHLhzMOQqHxH4unKhrCg3UIYFavUhA2P9YxNnSAZf3BA2ZqssWFM4oGWOuMVk; xt=gAAAAABe5gHguUd6WchKlHVwWppjVqejUkIlEJuSUNA_gQJh7BV7SdX3k6G6aqtjVRgJMyq2yVTEdqm-i9Hyy5NwZD5Je2o45xRPIwaOntUpEfj7lTxdlys; xt_expires_in=604800; identity=1',
                    'Host': 'hncu.xuetangx.com',
                    'If-Modified-Since': '0',
                    'Referer': 'https://hncu.xuetangx.com/manager',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'x-referer': 'https://hncu.xuetangx.com/manager#/studentCourselist',
                    'X-Requested-With': 'XMLHttpRequest',}
        url = "https://hncu.xuetangx.com/mycourse_list"
        getData = {'running_status': '',
                    'term_id': term,
                    'search': '',
                    'page_size': '10',
                    'page': '1',}
        response = requests.get(url,params=getData,headers=header)
        response = response.json()
        print(response['message'])
        list = response['data']['results']
        for item in list:
            self.class_list[item['course_id']] = item['class_id']


    def get_classID(self,cid):
        ssl._create_default_https_context = ssl._create_unverified_context
        post_url = "https://hncu.xuetangx.com/lms/api/v1/course/{}/courseware/".format(cid)
        payload = {"class_id": self.class_list[cid]}  # 可以通过修改这个去进行课程答案的查询81644 81651
        post_header = { 'Accept': 'application/json, text/plain, */*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Length': '20',
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Cookie': 'UM_distinctid=171957d590514c-05fb3675daf1cf-5313f6f-144000-171957d59063ba; plat_id=231; org_id=392; mode=1; CNZZDATA1273255756=1907010495-1587345719-null%7C1592129746; access_token=gAAAAABe5gHg9caBHJ5pHkbz47pFzLbp-tY9NBJ9wwuXGpqCv1drO7VSAOGHLhzMOQqHxH4unKhrCg3UIYFavUhA2P9YxNnSAZf3BA2ZqssWFM4oGWOuMVk; xt=gAAAAABe5gHguUd6WchKlHVwWppjVqejUkIlEJuSUNA_gQJh7BV7SdX3k6G6aqtjVRgJMyq2yVTEdqm-i9Hyy5NwZD5Je2o45xRPIwaOntUpEfj7lTxdlys; xt_expires_in=604800; identity=1',
                        'Host': 'hncu.xuetangx.com',
                        'If-Modified-Since': '0',
                        'Origin': 'https://hncu.xuetangx.com',
                        'Referer': 'https://hncu.xuetangx.com/lms',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                        'x-referer': 'https://hncu.xuetangx.com/lms#/24823/50157/schedule',
                        'X-Requested-With': 'XMLHttpRequest',}
        response = requests.post(post_url, data=json.dumps(payload), headers=post_header)
        html = response.json()
        if response.status_code == 200:
            for it in range(len(html["data"])):
               try:
                    list_course = html["data"][it]["homeworkRecord"]["all"]
                    for page_id in list_course:
                        self.view_answer(page_id)
               except Exception as e:
                    print("******************************************")

    def view_answer(self,page_id):
        header = {  'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Cookie': 'UM_distinctid=171957d590514c-05fb3675daf1cf-5313f6f-144000-171957d59063ba; plat_id=231; org_id=392; mode=1; CNZZDATA1273255756=1907010495-1587345719-null%7C1592129746; access_token=gAAAAABe5gHg9caBHJ5pHkbz47pFzLbp-tY9NBJ9wwuXGpqCv1drO7VSAOGHLhzMOQqHxH4unKhrCg3UIYFavUhA2P9YxNnSAZf3BA2ZqssWFM4oGWOuMVk; xt=gAAAAABe5gHguUd6WchKlHVwWppjVqejUkIlEJuSUNA_gQJh7BV7SdX3k6G6aqtjVRgJMyq2yVTEdqm-i9Hyy5NwZD5Je2o45xRPIwaOntUpEfj7lTxdlys; xt_expires_in=604800; identity=1',
                    'Host': 'hncu.xuetangx.com',
                    'If-Modified-Since': '0',
                    'Referer': 'https://hncu.xuetangx.com/lms',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                    'x-referer': 'https://hncu.xuetangx.com/lms#/24823/50157/homeworkList/analysis/P+24823+0001/H+24823+001',
                    'X-Requested-With': 'XMLHttpRequest'}
        #https://hncu.xuetangx.com/inner_api/homework/score/result/P%2B29698%2B0090/H+24823+159
        ssl._create_default_https_context = ssl._create_unverified_context
        url = "https://hncu.xuetangx.com/inner_api/homework/score/result/P%2B29698%2B0090/{}/".format(page_id)
        response = requests.get(url,headers=header)
        response = response.json()
        print(response['data']['descriptions'])
        for it in range(len(response['data']['question_data'])):
            print(response['data']['question_data'][it]['correct_answer'])

    def start(self):
        self.showTheme()
        self.term_id = input("请输入学期代号:")
        self.get_class(self.term_list[self.term_id])
        while True:
            cid = input("请输入你要刷的课程ID号:")
            self.get_classID(int(cid))



if __name__ == '__main__':
   brain = xuetangyun_videp()
   brain.start()
