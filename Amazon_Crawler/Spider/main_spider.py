from PyQt5.QtCore import QThread, pyqtSignal
from Spider import Getter
from Spider import Word_Statis
from threading import Thread,Lock
import queue
import os

q = queue.Queue()
lock = Lock()
getter = Getter.Getter()
cal_words = Word_Statis.Cal_Words()


class all_title_spider(QThread):
    # 使用信号和UI主线程通讯
    signal = pyqtSignal(str)

    def __init__(self, inputs_lst, file_path):
        super(all_title_spider, self).__init__()
        self.inputs = inputs_lst  #textEdit，set格式
        self.file_path = file_path
        # self.file = time  # 设置延时时间

    def crawl_one(self,q):
        '''
        抓取一个url的title信息并保存到file中
        :param url:
        :param file:
        :return:
        '''
        while q.empty() is not True:
            lock.acquire()#加锁
            crawler_tuple = q.get()
            lock.release()#解锁
            url = crawler_tuple[0]
            file = crawler_tuple[1]
            self.signal.emit('开始抓取: {url}'.format(url=url))
            inf_iter = getter.start_crawl(url)
            if inf_iter != None:
                for inf in inf_iter:
                    lock.acquire()  # 加锁
                    self.signal.emit('已抓取: {inf}...'.format(inf=str(inf)))
                    getter.title_save(inf, file)
                    lock.release()  # 解锁

    def run(self):
        global file
        self.inputs_set = set([i for i in self.inputs if i != '' and i != None])
        if len(self.inputs_set) == 1:
            file = getter.mk_file(self.file_path, str(self.inputs[0]))
            # print('工作目录为: {file}'.format(file=file))
            self.signal.emit('工作目录为: {file}'.format(file=file))
            for input in self.inputs_set:
                need_crawl = input.strip().replace('\n', '')
                new_file = file + '/' + input + '.txt'
                if isinstance(need_crawl, str) and len(need_crawl) != 0:
                    url_lst = getter.mk_url(need_crawl)
                    for url in url_lst:
                        self.signal.emit('生成{url}'.format(url=url))
                        q.put((url, new_file))
                    # self.crawl_one(need_crawl, file)
        else:
            #多个输入
            file = getter.mk_file(self.file_path, 'manyinputs_' + str(self.inputs[0]))
            # print('工作目录为: {file}'.format(file=file))
            self.signal.emit('工作目录为: {file}'.format(file=file))
            for input in self.inputs_set:
                need_crawl = input.strip().replace('\n', '')
                new_file = file + '/' + input + '.txt'
                if isinstance(need_crawl, str) and len(need_crawl) != 0:
                    url_lst = getter.mk_url(need_crawl)
                    for url in url_lst:
                        self.signal.emit('生成{url}'.format(url=url))
                        q.put((url, new_file))
        p_lst = []
        #开始多线程抓取
        for i in range(6):
            p = Thread(target=self.crawl_one, args=(q,))  # 注意args里面要把q对象传给我们要执行的方法，这样子进程才能和主进程用Queue来通信
            p.start()
            p_lst.append(p)
        for p in p_lst:
            p.join()
        self.signal.emit('数据抓取完毕，开始进行词频统计')
        #进行文件合并

        # 将保存好的title进行词频统计
        if os.listdir(file) != []:
            cal_words.statis_word_reviews(file)
        else:
            self.signal.emit('未抓取到title信息')
        # print('程序运行完毕,数据保存路径为：{file}'.format(file=file))
        self.signal.emit('程序运行完毕\n数据保存路径为：{file}'.format(file=file))


if __name__ == '__main__':
    spider = all_title_spider(['3480728011'])
    spider.run()