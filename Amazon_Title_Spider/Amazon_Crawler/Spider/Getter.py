from Spider import send_request, crawl_info
import os
import logging
# from loguru import logger
import datetime

# sr = send_request.Send_Request()
spider = crawl_info.Spider()

base_path = os.path.dirname(os.path.abspath(__file__))
today_file = str(datetime.date.today())
work_file = '..\\logs\\' + today_file + '.log'
log_path = os.path.join(base_path, work_file)
logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename = log_path,
                    filemode = 'a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
# a是追加模式，默认如果不写的话，就是追加模式
                    )
class Getter(send_request.Send_Request):

    def mk_file(self, base_file, input):
        path = base_file
        work_file = str(datetime.date.today())
        work_path = os.path.join(path, work_file)
        if not os.path.exists(work_path):
            os.makedirs(work_path)
        keywordpath = os.path.join(work_path, str(input))
        #判断关键字文件夹如果存就删除文件夹内文件
        if os.path.exists(keywordpath) and os.listdir(keywordpath)!=[]:
            file_lst = os.listdir(keywordpath)
            for file in file_lst:
                file_path = os.path.join(keywordpath, file)
                os.remove(file_path)
        elif os.path.exists(keywordpath) and os.listdir(keywordpath)==[]:
            logging.debug('文件夹{file}已经存在'.format(file=keywordpath))
        else:
            # 创建关键词文件夹
            os.makedirs(keywordpath)
        return keywordpath

    def mk_url(self, inputs):
        '''
        根据输入生成链接
        :param inputs: 输入、可以是关键字或类目代码
        :return: url 列表
        '''
        if inputs.isdigit():
            page_one = 'https://www.amazon.com/gp/bestsellers/{inputs}'.format(inputs=inputs)
            page_two = self.bsr_two_url(page_one)
            if page_two == '无效链接':
                url_lst = []
            else:
                url_lst = [page_one, page_two]
        elif inputs[:2] == 'B0':
            url_lst = ['https://www.amazon.com/dp/{inputs}/'.format(inputs=inputs)]
        else:
            url_lst = ['https://www.amazon.com/s?k={inputs}&page={p}'.format(inputs=inputs, p=p) for p in range(1, 4)]
        return url_lst

    def title_save(self, inf, file_path):
        '''
        :param inf: dict 包含了title和reviews
        :param file: 文件夹位置
        :return:
        '''
        if inf.get('title') == None:
            print('此次未抓取到title')
            return
        path = file_path
        if not os.path.exists(path):
            with open(path, 'a', encoding='utf-8') as f:
                f.write('\t'.join(inf.keys()) + '\n')
        with open(path, 'a', encoding='utf-8') as f:
            l = [str(i) for i in list(inf.values())]
            f.write('\t'.join(l) + '\n')
            # print('>>>>已抓取：{title}....<<<<<'.format(title=inf['title'][:20]))


    def bsr_two_url(self, page_one_url):
        '''
        获取bsr页面的第二页链接
        :param page_one_url: bsr页面的第一页链接
        :return:
        '''
        page_one_txt = self.get_html(page_one_url)
        if page_one_txt != None:
            response = (page_one_txt, page_one_url)
            page_two = spider.get_bsr_two_url(response)
            if page_two != []:
                return page_two[0]
            else:
                print('此类目 {page_one_url} 无第二页链接'.format(page_one_url=page_one_url))
                return
        else:
            # print(f'{page_one_url}为无效链接')
            return '无效链接'


    def start_crawl(self, url):
        '''
        用于生成一个返回（title, reviews）的生成器
        通过判断url中是否包含特定字符来选择解析方式
        :param url: 起始url，
        :return:
        '''
        if url != None:
            start_text = self.get_html(url)
            if isinstance(start_text, str):
                if 'https://www.amazon.com/s?k=' in url:
                    response = (start_text, url)
                    info_iter = spider.get_page_title(response)
                elif 'dp/B0' in url:
                    response = (start_text, url)
                    info_iter = spider.get_detail_inf(response)
                else:
                    # spider.check('asin','sss', start_text)
                    response = (start_text, url)
                    info_iter = spider.get_bsr_title(response)
                return info_iter
            else:
                # print(f'此{url}为无效页面')
                return


if __name__ == '__main__':
    getter = Getter()
    input = 'cat'
    file =getter.mk_file(input)
    # url = 'https://www.amazon.com/gp/bestsellers/lawn-garden/ref=pd_zg_ts_lawn-garden'
    lst = getter.mk_url(input)
    print(lst)
    for url in lst:
        if url != None:
            inf_iter = getter.start_crawl(url)
            # print(inf_iter)
            for inf in inf_iter:
                getter.title_save(inf, file)
                print(inf)



