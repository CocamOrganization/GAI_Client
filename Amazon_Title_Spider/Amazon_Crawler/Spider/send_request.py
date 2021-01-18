from os import path
import sys
sys.path.append(path.abspath('D:/software/Lib/site-packages'))
import requests
import json
import logging as logger
# from loguru import logger
import random
import os
import time
import re
import datetime

proxypool_url = 'http://127.0.0.1:5555/random'

base_path = os.path.dirname(os.path.abspath(__file__))
today_file = str(datetime.date.today())
work_file = '..\\logs\\' + today_file + '.log'
log_path = os.path.join(base_path, work_file)
# logger.add(log_path, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

class Send_Request(object):
    def __init__(self):
        '''headers::浏览器头
                       path :: 文件路径
                       keyword::关键词
                    '''
        self.headers = {'user-agent': self.user_agent(),
                        'accept-ch': 'ect, rtt, downlink',
                        'accept - ch - lifetime': '86400',
                        'cache - control': 'no - cache',
                        'content - encoding': 'gzip',
                        'cookies':'session-id-time=2082787201l; session-id=145-3415291-9452431; ubid-main=133-2917423-5668454; skin=noskin; lc-main=en_US; session-token=ujpcqr+aN+C3smObVg5HAnsCvEuSCoFHPvpfypVS2gQf/iOqS1lMYQfRhDV1dal3bWLSkuP4KIQNYiEVjRAC87mAarCxsJjHaUXUXKonDYpmy73aUFtXroWS0ll6ryZMk2dpv/bKQ49thMq9+btI7HZAWizkt60yT22oirQUpcQZs0BxOm5EH7nM5e7UXkdO; csm-hit=tb:3CQH6QBB95NWPTEM33VV+s-3CQH6QBB95NWPTEM33VV|1609383705050&t:1609383705050&adb:adblk_no',
                        'content - language': 'en-US',
                        'content - type': 'text/html',
                        'referer': 'https://www.amazon.com/',
                        'charset': 'UTF-8',
                        'server': 'Server'}
        self.US_data = {'locationType': 'LOCATION_INPUT',
                         'zipCode': '10001',
                         # 'countryCode': 'JP',
                         'deviceType': 'web',
                         'pageType': 'Detail',
                         'actionSource': 'glow'}

        self.CN_data = {'locationType': 'COUNTRY',
                        'district': 'JP',
                        'countryCode': 'JP',
                        'deviceType': 'web',
                        'pageType': 'Detail',
                        'actionSource': 'glow',
                        'almBrandId': 'undefined'}

    def get_random_proxy(self):
        """
        get random proxy from proxypool
        :return: proxy
        """
        return requests.get(proxypool_url).text.strip()

    def user_agent(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, 'user_agent.txt')
        # path = 'D:/Demo/Amazon-Commodity/config/user_agent.txt'
        with open(path, 'r', encoding='utf-8') as f:
            ua_st = f.readlines()
        return random.choice(ua_st).strip('\n')

    def get_csr_token(self, text):
        '''
        用于查找程序中被分配的token值
        '''
        pattern = 'CSRF_TOKEN : "(.*?)"'
        CSRF_TOKEN = re.search(pattern, text).group(1)
        # print(CSRF_TOKEN)
        print('提取token：{CSRF_TOKEN}'.format(CSRF_TOKEN=CSRF_TOKEN))
        address_headers = {'authority': 'www.amazon.com',
                           'method': 'POST',
                           'path': '/gp/delivery/ajax/address-change.html',
                           'scheme': 'https',
                           'accept': 'text/html,*/*',
                           'accept-encoding': 'gzip, deflate, br',
                           'accept-language': 'zh-CN,zh;q=0.9',
                           'content-length': '139',
                           'content-type': 'application/x-www-form-urlencoded',
                           'contenttype': 'application/x-www-form-urlencoded;charset=utf-8',
                           'downlink': '0.65',
                           'anti-csrftoken-a2z': CSRF_TOKEN,
                           'cookies':'session-id-time=2082787201l; session-id=145-3415291-9452431; ubid-main=133-2917423-5668454; skin=noskin; lc-main=en_US; session-token=ujpcqr+aN+C3smObVg5HAnsCvEuSCoFHPvpfypVS2gQf/iOqS1lMYQfRhDV1dal3bWLSkuP4KIQNYiEVjRAC87mAarCxsJjHaUXUXKonDYpmy73aUFtXroWS0ll6ryZMk2dpv/bKQ49thMq9+btI7HZAWizkt60yT22oirQUpcQZs0BxOm5EH7nM5e7UXkdO; csm-hit=tb:3CQH6QBB95NWPTEM33VV+s-3CQH6QBB95NWPTEM33VV|1609383705050&t:1609383705050&adb:adblk_no',
                           'ect': '3g',
                           'origin': 'https://www.amazon.com',
                           'referer': 'https://www.amazon.com/dp/B07KDXQTJV?th=1',
                           'rtt': '600',
                           'sec-fetch-dest': 'empty',
                           'sec-fetch-mode': 'cors',
                           'sec-fetch-site': 'same-origin',
                           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                           'x-requested-with': 'XMLHttpRequest'}
        return address_headers

    def cookies(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, 'cookies_17.txt')
        # path = 'D:/Demo/Amazon-Commodity/config/cookies_17.txt'
        with open(path, 'r', encoding='utf-8') as f:
            cookies_17 = f.read()
        cookies_py = json.loads(cookies_17)
        cookie = random.choice(cookies_py)
        return self.tranfer(cookie)

    def tranfer(self, cookie):
        cookie = [item['name'] + "=" + item['value'] for item in cookie]
        cookiestr = '; '.join(item for item in cookie)  # 每一句‘name’+'value'后面都要加分号和空格，格式不正确不能使用，牢记牢记
        return cookiestr

    def check(self, reason, asin, text):
        '''将抓取失败的html文件保存到本地，分析原因'''
        path = 'D:/test/' + reason+ '/' + asin + '.html'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)


    def get_html(self, url, retries=0):
        '''获取html代码'''
        if retries > 999:
            print('超过最大重试次数:{url}'.format(url=url))
            return
        retries += 1
        adress_url = 'https://www.amazon.com/gp/delivery/ajax/address-change.html'
        address_selection = 'https://www.amazon.com/gp/glow/get-address-selections.html?deviceType=desktop&pageType=Detail'
        session = requests.Session()
        try:
            #bestseller页面和详情页分开抓取
            if 'dp/B0' not in url:
                response = requests.get(url, headers=self.headers, timeout=5)
            else:
                token_response = session.get(address_selection, headers=self.headers, timeout=10)
                if token_response.status_code == 200:
                    address_headers = self.get_csr_token(token_response.text)
                time.sleep(random.randint(1, 2))
                session.post(adress_url, data=self.US_data, headers=address_headers, timeout=10)#修改地址
                # self.check('asin', 'tt', b.text)
                response = session.get(url, headers=self.headers, timeout=5)
            text = response.text
            if 'Robot Check' in text:
                print('出现验证码,更换ip:{url}'.format(url=url))
                time.sleep(random.randint(4,10))
                return self.get_html(url, retries)
            elif 'Enter the characters you see below' in text:
                print('出现验证码,更换ip:{url}'.format(url=url))
                time.sleep(random.randint(4, 10))
                return self.get_html(url, retries)
            elif response.status_code == 404:
                print('Page Not Found: {url}'.format(url=url))
            elif response.status_code == 200:
                print('成功获取页面：{url}'.format(url=url))
                return text
            elif response.status_code == 503:
                print('出现503错误：{url}'.format(url=url))
                # self.check('unknown', '503', text)
                time.sleep(random.randint(6, 10))
                return self.get_html(url, retries)
            else:
                print('出现未知类型的错误：{url}'.format(url=url))
                # self.check('unknown', url, text)
        except:
            print('连接超时，准备重试')
            time.sleep(random.randint(8, 12))
            return self.get_html(url, retries)

if __name__ == '__main__':
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    print(base_path)
    path = os.path.join(base_path,'..\\config\\user_agent.txt')
    print(path)
    print(path)
    print(os.getcwd())
    sr = Send_Request()
    print(sr.user_agent())
