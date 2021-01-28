import pandas as pd
import numpy as np
import itertools
import os
import logging
import datetime

base_path = os.path.dirname(os.path.abspath(__file__))
today_file = str(datetime.date.today())
work_file = '..\\logs\\' + today_file + '.log'
log_path = os.path.join(base_path, work_file)
logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename = log_path,
                    filemode = 'a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
# a是追加模式，默认如果不写的话，就是追加模式
                    )

class Cal_Words(object):
    def word_count(self, Split_Keywords):
        '''
        本函数用于统计词频

        参数：
            Split_Keywords: 需要统计词频的Series
        '''
        Word_Count = Split_Keywords.value_counts()#统计单词个数
        Word_Count = Word_Count.reset_index()#将Series化为DataFrame
        Word_Count.columns = ['keywords', 'times']
        return Word_Count

    def split_words_one(self, keywords):
        '''
        本函数用于将keywords序列按照一个单词进行分词
        :param keywords: Series类型
        :return:
        '''
        Split_Keywords = keywords.apply(
            lambda x: x.replace('，', ' ').replace(':', ' ').replace(')', ' ').replace('(', ' ').replace(',',
                                                                                                        ' ').replace(
                '/', ' ').replace('\'', '').replace('\"', '').replace('-', ' ').replace('+', ' ').replace('#',
                                                                                                          '').replace(
                '   ', ' ').replace('  ', ' ').strip()).apply(lambda x: x.split(' '))
        return Split_Keywords

    def words_number_count(self, keywords):
        '''
        本函数用于统计每个搜索词的单词个数

        参数：
            keywords: 需要进行统计词个数的关键词,Series格式
        '''
        Split_Keywords = self.split_words_one(keywords)
        words_number = Split_Keywords.str.len()
        return words_number

    def get_iter(self, keywords, k):
        '''
        本函数用于按照k个单词进行分词
        keywords::List对象,元素为按单个词分割后的列表
        k::按k个单词进行分词，需要被分割为包含k个关键字词组
        return:: List对象，包含被分割好的词组
        '''
        x_len = len(keywords)
        Lst = []
        for i in range(x_len - k + 1):
            Lst.append(' '.join(keywords[i:i + k]))
        return Lst

    def split_keywords_k(self, keywords, k):
        '''
        本函数用于按k个单词进行分词

        参数：
            keywords: get_keywords函数的结果，Series
            k: 按k个单词进行分词
        '''
        words_num = self.words_number_count(keywords)#keywords包含多少个单词,series格式
        Index = words_num >= k #查看单词总数是否大于要被分的个数
        # 若k大于全部的词，则返回-1
        if sum(Index) == 0:
            return -1
        # 筛选出需要被分割处理的单词的index,得到需要处理的词
        Index = np.array(keywords.index[Index])
        # 先进行一个词的分词
        Split_Keywords = self.split_words_one(keywords)
        # 得到需要处理的词
        Split_Keywords = Split_Keywords[Index]
        # 进行k分词
        Split_Keywords_k = Split_Keywords.apply(lambda x: self.get_iter(x, k))
        list_1 = list(Split_Keywords_k)
        list_2 = list(itertools.chain(*list_1))
        Split_Keywords_k = pd.Series(list_2)
        return Split_Keywords_k

    def split_keywords_k2(self, keywords_reviews, k):
        '''
        本函数用于按k个单词进行分词

        参数：
            keywords: get_keywords函数的结果，DataFrame
            k: 按k个单词进行分词
        '''
        keywords_copy = keywords_reviews.add_suffix('_copy')
        keywords = keywords_reviews['title']
        words_num = self.words_number_count(keywords)#keywords包含多少个单词,series格式
        Index = words_num >= k #查看单词总数是否大于要被分的个数
        # 若k大于全部的词，则返回-1
        if sum(Index) == 0:
            return -1
        # 筛选出需要被分割处理的单词的index,得到需要处理的词
        Index = np.array(keywords.index[Index])
        # 先进行一个词的分词
        Split_Keywords = self.split_words_one(keywords)
        # 得到需要处理的词
        Split_Keywords = Split_Keywords[Index]
        # 进行k分词
        Split_Keywords_k = Split_Keywords.apply(lambda x: self.get_iter(x, k))
        # 将分好词的Series 与 title 和 reviews进行拼接， 并获取title和reviws列
        Split_Keywords_k = keywords_copy.join(Split_Keywords_k, how='inner')[['title', 'reviews_copy']]
        list1 = Split_Keywords_k.values.tolist()
        title_review_lst = [[title, list_value[1]] for list_value in list1
                            for title in list_value[0]]
        title_review_frame = pd.DataFrame(title_review_lst)
        title_review_frame.columns = ['title', 'reviews']
        return title_review_frame

    def cal_save_words(self, df, writer):
        '''
        统计reviews和count并保存到excel
        :param df: 需要处理的dataframe
        :param writer: 写入本地excel位置
        :return:
        '''
        for i in range(1, 11):
            Split_Keywords = self.split_keywords_k2(df, i)  # DataFrame格式，带keyword和reviews
            if type(Split_Keywords) != int:  # title的单词个数大于需要被划分的词组个数
                Word_reviews = Split_Keywords.groupby(['title']).sum()  # 统计reviews
                Word_count = Split_Keywords['title'].value_counts()
                Word_count.name = 'count'
                word_statis = Word_reviews.join(Word_count, how='outer')
                word_statis = word_statis.sort_values(by=['count', 'reviews'], ascending=False)
                word_statis.to_excel(writer, sheet_name=str(i) + '个词')
        writer.save()
        writer.close()

    def statis_word_reviews(self, file_path):
        '''
        用于保存词频统计的结果
        :param file_path: 文件夹路径
        :return:
        '''
        os.chdir(file_path)
        path_all = os.listdir()
        path_txt = []
        logging.info('开始读取{path}中的文件'.format(path=file_path))
        for i in path_all:
            if i[-3:] == 'txt':
                path_txt.append(i)
        keyword_all = pd.DataFrame()
        for path in path_txt:
            keywords = pd.read_csv(path, sep='\t')
            keyword_all = pd.concat([keywords, keyword_all], axis=0)
            keywords['reviews'] = keywords['reviews']. \
                replace(',', '').replace('None', '0').astype(np.int64)
            if len(keywords) == 0:
                logging.debug('未成功抓取到title')
                return
            writer = pd.ExcelWriter(path[:path.find('.')] + '词频统计报告.xls')
            self.cal_save_words(keywords, writer)
        if len(path_txt)>1:
            logging.info('开始进行全部词频统计：{path}'.format(path=file_path))
            writer = pd.ExcelWriter('全部词频统计报告.xls')
            self.cal_save_words(keyword_all, writer)




    def statis_word_numbers(self, file_path):
        '''
        用于保存词频统计的结果
        :param file_path: 文件夹路径
        :return:
        '''
        read_path = file_path + '/all_titles.txt'
        path = file_path + '/词频统计.xls'
        keywords = pd.read_csv(read_path, sep='\t')['title']
        if len(keywords) == 0:
            logging.debug('未成功抓取到title')
            return
        writer = pd.ExcelWriter(path)
        for i in range(1, 11):
            Split_Keywords = self.split_keywords_k(keywords, i)
            if type(Split_Keywords) != int:#title的单词个数大于需要被划分的词组个数
                Word_Count = self.word_count(Split_Keywords)
                Word_Count.to_excel(writer, sheet_name=str(i) + '个词')
        writer.save()
        writer.close()

if __name__ == '__main__':
    cal_words = Cal_Words()
    # keywords = pd.read_table('D:/cat food_page_title.txt', header=None).iloc[:, 1]
    # word_number = cal_words.words_number_count(keywords)
    # words_k = cal_words.split_keywords_k(keywords, 3)
    # print(words_k)
    # word_count = cal_words.word_count(words_k)
    # print(word_count)
    cal_words.statis_word_reviews('C:/Users/86178/Desktop/词频抓取/2021-01-27\cats')