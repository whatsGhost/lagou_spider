# coding=utf-8

import re,json
import requests
from file import File

class Spider:
    headers = {
            "X-Requested-With": 'XMLHttpRequest',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            #"Origin": 'https://www.lagou.com',
            "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
            "Connection": 'keep-alive'
            }

    def __init__(self,search,city):
        self.search = search
        self.city = city

    def __getPage(self):
        url = 'https://www.lagou.com/jobs/list_'+self.search+'?city='+self.city+'&cl=false&fromSearch=true&labelWords=&suginput='
        html = requests.get(url,headers =self.headers)
        html.encoding = 'utf-8'
        rst = re.search(r'<span class="span totalNum">\d\d',html.text)
        if not rst:
            rst = re.search(r'<span class="span totalNum">\d',html.text)
        return  int(rst.group()[28:])

    def analyse(self):
        pageCount = self.__getPage()
        for i in range(1,pageCount+1):
            print '\n*****************************第'+str(i)+'页*********************************\n'
            url = 'http://www.lagou.com/jobs/positionAjax.json?city='+self.city+'&first='+'true'+'&kd='+self.search+'&pn='+str(i)
            html = requests.get(url,headers =self.headers)
            html.encoding = 'utf-8'
            htmlFile = File("test.html")
            data = json.loads(html.text)
            for workmsg in data['content']['positionResult']['result'] :
                print workmsg['positionName'] +':\t----'+ workmsg['companyShortName'] + workmsg['salary'] + workmsg['financeStage'] + workmsg['workYear']