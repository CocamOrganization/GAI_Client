import random
import json
import os

class UserAgent1(object):
    def __init__(self):
        pass

    def user_agent(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'user_agent.txt')
        with open(path, 'r', encoding='utf-8') as f:
            ua_st = f.readlines()
        return random.choice(ua_st).strip('\n')

    def cookies(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'cookies_17.txt')
        # path = 'D:/Demo/title_Spider/cookies_17.txt'
        with open(path, 'r', encoding='utf-8') as f:
            cookies_17 = f.read()
        # print(cookies_17)
        cookies_py = json.loads(cookies_17)
        cookie = random.choice(cookies_py)
        return self.tranfer(cookie)

    def tranfer(self, cookie):
        cookie = [item['name'] + "=" + item['value'] for item in cookie]
        cookiestr = '; '.join(item for item in cookie)  # 每一句‘name’+'value'后面都要加分号和空格，格式不正确不能使用，牢记牢记
        return cookiestr

if __name__ == '__main__':
    ua = UserAgent1()
    print(ua.cookies())
