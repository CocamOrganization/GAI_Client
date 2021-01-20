import datetime
from lxml import etree
import logging as logger
# from loguru import logger
import os
# from os import path
import re

base_path = os.path.dirname(os.path.abspath(__file__))
today_file = str(datetime.date.today())
work_file = '..\\logs\\' + today_file + '.log'
log_path = os.path.join(base_path, work_file)
# logger.add(log_path, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

class Spider(object):

    def check(self, reason, asin, text):
        '''将抓取失败的html文件保存到本地，分析原因'''
        path = 'D:/test/' + reason+ '/' + asin + '.html'
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

    def get_stars(self, ASIN):
        star_url = 'https://www.amazon.com/gp/customer-reviews/widgets/' \
                   'average-customer-review/popover/ref=dpx_acr_pop_?conte' \
                   'xtId=dpx&asin={asin}'.format(asin=ASIN)
        sr = send_request.Send_Request()
        text = sr.get_html(star_url)
        response = etree.HTML(text)
        detail_stars = response.xpath(
            '//tr[@class="a-histogram-row a-align-center"]/td[@class="a-text-right a-nowrap"]//a/@title')
        return detail_stars

    def match_asin(self, strings):
        pattern = '/dp/(B.*?)/'
        asin = re.search(pattern, strings.replace('%2F', '/')).group(1)
        return asin

    def match_kind(self, strings):
        pattern = 'bs_(\d*?)_(\d*?)\?'
        kind = re.search(pattern, strings).group(1)
        rank = re.search(pattern, strings).group(2)
        return kind, rank

    def match_img(self, strings):
        pattern = '(https.*?\.jpg)'
        img = re.search(pattern, strings).group(1)
        return img

    # @logger.catch
    def get_detail_inf(self, Responses):
        '''
        :param Response: tuple :(text, url)
        :param cocam: 判断是否为cocam产品
        :return: dict
        '''
        text = Responses[0]
        url = Responses[1]
        response = etree.HTML(text)
        commodity_info = {}
        #收货地址
        # address = response.xpath('//span[@id="glow-ingress-line2"]/text()')
        # if  address==[]:
        #     logger.debug('No Address:{url}'.format(url=url))
        #     Responses = ('No Address', url)
        #     return Responses
        # elif 'New York 10001' not in address[0]:
        #     logger.debug('This Page Not 10001:{url}'.format(url=url))
        #     Responses = ('Page Not 10001', url)
        #     return Responses
        #详情页链接
        # commodity_info['url'] = url
        # # 商品类目与排名
        # try:
        #     commodity_info['kinds_of_commodity'] = response.xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]//li/span/a/text()')[-1].\
        #         replace('\n', '').strip()
        # except:
        #     commodity_info['kinds_of_commodity'] = None
        # 标题
        try:
            commodity_info['title'] = response.xpath('//span[@id="productTitle"]/text()')[0].strip('\n')
        except:
            commodity_info['title'] = None
        # Asin
        # try:
        #     commodity_info['ASIN'] = self.match_asin(url)
        # except:
        #     print('无效页面')
        #     # self.check('asin', 'no', text)
        #     return
        # # 产品店铺
        # try:
        #     shop = response.xpath('//a[@id="bylineInfo"]/text()')[0]
        #     commodity_info['shop'] = shop.replace('Brand: ', '').replace('Visit the ', '').replace(' Store', '')
        #     # print(commodity_info['shop'])
        # except:
        #     commodity_info['shop'] = None
        # # 产品评分
        # try:
        #     commodity_info['score'] = float(response.xpath('//span[@id="acrPopover"]/@title')[0].split(' ')[0])
        #     # commodity_info['Manufacturer'] = response.xpath('//span[@id="acrPopover"]/@title').extract_first()
        #     # print(commodity_info['score'])
        # except:
        #     commodity_info['score'] = None
        #
        # try:
        #     is_available= response.xpath('//span[@class="a-color-price a-text-bold"]/text()')[0]
        #     if is_available == 'Currently unavailable.':
        #         commodity_info['available'] = 'Currently unavailable.'
        #     else:
        #         commodity_info['available'] = 'UnKnown'
        #         # print(commodity_info['available'])
        # except:
        #     commodity_info['available'] = None
        # # 产品排名
        # try:
        #     rank1 = response.xpath('//span/a[contains(@href, "bestseller")]/../text()')
        #     rank2 = response.xpath('//li[@id="SalesRank"]//text()')
        #     ranks = rank1 + rank2
        #     fliter_rank = [rank for rank in ranks if '#' in rank]
        #     commodity_info['father_rank'] = fliter_rank[0]
        # except:
        #     commodity_info['father_rank'] = None
        # # 8.日期
        # commodity_info['date'] = str(datetime.date.today())
        # # 打分评级
        # try:
        #     detail_stars = response.xpath(
        #         '//tr[@class="a-histogram-row a-align-center"]/td[@class="a-text-right a-nowrap"]//a/@title')
        #     if detail_stars==[]:
        #         detail_stars = self.get_stars(commodity_info['ASIN'])
        #     for star in detail_stars:
        #         name = star.split('represent')[0].strip(' ').replace(' ', '_')
        #         score_h = star.split('represent')[1].split('of')[0].strip(' ')
        #         score = float(score_h.replace('%', '')) / 100
        #         commodity_info[name] = score
        #     # print(commodity_info['detail_score'])
        # except:
        #     print('无人评分')

        # 评论数
        try:
            commodity_info['reviews'] = int(response.xpath(
                '//span[@id="acrCustomerReviewText"]/text()')[0].split()[0].replace(',', ''))
            # print(commodity_info['reviews'])
        except:
            commodity_info['reviews'] = 0
        # # 价格
        # try:
        #     commodity_info['price'] = response.xpath('//span[contains(@id,"priceblock")]/text()')[0]
        # except:
        #     commodity_info['price'] = None
        #     # self.check('price',commodity_info['ASIN'], text)
        # # 图片
        # try:
        #     img_element = response.xpath('//div[@id="imgTagWrapperId"]/img')[0]
        #     img_str = etree.tostring(img_element)
        #     img_url = self.match_img(str(img_str, encoding='utf-8'))
        #     commodity_info['img'] = img_url
        # except:
        #     commodity_info['img'] = None
        # # 第一次上架时间
        # try:
        #     commodity_info['Date_First_Available'] = \
        #     response.xpath("//th[contains(text(),'Date First Available')]/following-sibling::td/text()")[0].strip('\n')
        # except:
        #     commodity_info['Date_First_Available'] = None
        # # 是否打折
        # try:
        #     commodity_info['Coupon'] = \
        #         response.xpath('//label[@id="couponBadge"]/text()"]/text()')[0].strip('\n')
        # except:
        #     commodity_info['Coupon'] = 'None'
        # # 商品颜色
        # try:
        #     commodity_info['color'] = len(response.xpath('//img[@class="imgSwatch"]'))
        # except:
        #     commodity_info['color'] = None
        # # 商品尺寸
        # try:
        #     commodity_info['size'] = len(response.xpath('//button[@class="a-button-text"]//span[@class="a-size-base"]'))
        # except:
        #     commodity_info['size'] = None
        # # 发货方式
        # try:
        #     commodity_info['sold_by'] = \
        #         response.xpath('//span[@class="tabular-buybox-text"]/text()')[0]#被谁售卖
        #     commodity_info['ships_from'] = \
        #         response.xpath('//span[@id="tabular-buybox-truncate-0"]//span[@class="tabular-buybox-text"]/text()')[0] #从何处发货
        #     # print(commodity_info['sold_by'], commodity_info['ships_from'])
        # except:
        #     commodity_info['sold_by'] = None
        #     commodity_info['ships_from'] = None
        #
        # #description描述详情
        # try:
        #     descriptions = response.xpath(
        #         '//ul[@class="a-unordered-list a-vertical a-spacing-mini"]//span[@class="a-list-item"]/text()')
        #     i = 0
        #     for description in descriptions:
        #         if description != '\n' and i < 5:
        #             i += 1
        #             index = 'description_{d}'.format(d=i)
        #             commodity_info[index] = description.strip('\n')
        # except:
        #     commodity_info['description_1'] = commodity_info['description_2'] = commodity_info[
        #         'description_3'] = None
        yield commodity_info

    # @logger.catch
    def get_bsr_url(self, Responses):
        '''
            :param response: tuple:(text, url)
            :return:
        '''
        text = Responses[0]
        response = etree.HTML(text)
        commodity_info = {}
        try:
            # 9爬虫的链接
            commodity_info['URL'] = response.xpath('//link[@rel="canonical"]/@href')[0]
        except:
            commodity_info['URL'] = None
        try:
            # 8.商品种类
            kinds_of_commodity = response.xpath('//div[@id="zg-right-col"]/h1/span/text()')[0]
            commodity_info['kinds_of_commodity'] = kinds_of_commodity
        except:
            commodity_info['kinds_of_commodity'] = None
        list_lis = response.xpath('//*[@id="zg-ordered-list"]//li')
        if list_lis:
            # print('list_lis 长度', len(list_lis))
            for each_li in list_lis:
                try:
                    # 1.详情页链接
                    link_normal = each_li.xpath(
                        './span/div/span/a[@class="a-link-normal"]/@href')[0]
                    commodity_info['ASIN'] = link_normal.split('/')[3]
                    # ASIN
                    commodity_info['ASIN'] = self.match_asin(link_normal)
                    commodity_info['link_normal'] = link_normal
                    # url_p = 'https://www.amazon.com/dp/' + commodity_info['ASIN']
                    # 2.产品名称
                    commodity_info['title'] = each_li.xpath('./span/div/span/a/span/div/img/@alt')[0]
                    # 7.图片
                    commodity_info['img'] = each_li.xpath('./span/div/span/a/span/div/img/@src')[0]
                    # 6.排名
                    commodity_info['Ranking'] = each_li.xpath('./span/div/div/span[1]/span/text()')[0]
                except:
                    commodity_info['ASIN'] = None
                    # self.check('bestseller',commodity_info['kinds_of_commodity'],text)
                # 8.日期
                commodity_info['date'] = str(datetime.date.today())
                # 3.评分
                try:
                    commodity_info['score'] = float(each_li.xpath(
                        './span/div/span/div[1]/a[1]/@title')[0].split(' ')[0])  # ['4,6 von 5 Sternen']
                except:
                    commodity_info['score'] = None
                # 4.评论数
                try:
                    commodity_info['reviews'] = int(
                        each_li.xpath('./span/div/span/div[1]/a[2]/text()')[0].replace(',', ''))
                except:
                    commodity_info['reviews'] = 0
                # 5.价格区间
                try:
                    commodity_info['price_Interval'] = '-'.join(each_li.xpath(
                        './/span[@class="p13n-sc-price"]/text()')) # 价格取最小值
                except:
                    commodity_info['price_Interval'] = None  # 有星级的价格
                bsr_title = (commodity_info['title'], commodity_info['reviews'])
                yield bsr_title
                cm_url = 'https://www.amazon.com' + commodity_info.get('link_normal', 'no_page')
                Request = (cm_url, 'bsr_url')
                yield Request

    # @logger.catch
    def get_page_url(self, Response):
        '''
        :param Rsponse: tuple:(text, url)
        :return: 首页titles
        '''
        text = Response[0]
        html = etree.HTML(text)
        a_ls = html.xpath('//a[@class="a-link-normal a-text-normal"]')
        for a in a_ls:
            if 'https://www.amazon.com/' in a.xpath('@href')[0]:
                href = a.xpath('@href')[0]
            else:
                href = 'https://www.amazon.com/' + a.xpath('@href')[0]
            Request = (href, 'page_url')
            yield Request

    # @logger.catch
    def get_page_title(self, Response):
        '''
        :param Rsponse: tuple:(text, url)
        :return: (title, reviews)
        '''
        text = Response[0]
        html = etree.HTML(text)
        commodity_info = {}
        a_ls = html.xpath('//a[@class="a-link-normal a-text-normal"]')
        for a in a_ls:
            href = a.xpath('@href')[0]
            try:
                commodity_info['title'] = \
                html.xpath('//a[contains(@href, "{href}") and @class="a-link-normal a-text-normal"]/span/text()'.format(href=href))[0]
            except:
                commodity_info['title'] = None
            try:
                commodity_info['reviews'] = int(html.xpath('//a[contains(@href, "{href}") and @class="a-link-normal"]/span/text()'.format(href=href))[0].replace(',', ''))
            except:
                commodity_info['reviews'] = 0
            yield commodity_info

    # @logger.catch
    def get_bsr_title(self, Responses):
        '''
            :param response: tuple:(text, url)
            :return:(title, reviews)
        '''
        text = Responses[0]
        commodity_info = {}
        response = etree.HTML(text)
        list_lis = response.xpath('//*[@id="zg-ordered-list"]//li')
        if list_lis:
            # print('list_lis 长度', len(list_lis))
            for each_li in list_lis:
                try:
                    # 1.产品名称
                    title = each_li.xpath('./span/div/span/a/div/@title')
                    if title == []:
                        title = each_li.xpath('./span/div/span/a/span/div/img/@alt')
                    commodity_info['title'] = title[0]

                except:
                    commodity_info['title'] = None
                # 4.评论数
                try:
                    commodity_info['reviews'] = int(
                        each_li.xpath('./span/div/span/div[1]/a[2]/text()')[0].replace(',', ''))
                except:
                    commodity_info['reviews'] = 0
                yield commodity_info

    def get_bsr_two_url(self, response):
        text = response[0]
        html = etree.HTML(text)
        bsr_two_url = html.xpath('//li[@class="a-normal"]/a/@href')
        return bsr_two_url




if __name__ == '__main__':
    import send_request
    sr = send_request.Send_Request()
    spider = Spider()
    # text = sr.get_html('https://www.amazon.com/dp/B08DK9X3XC')
    text = sr.get_html('https://www.amazon.com/gp/bestsellers/2975266011')
    # spider.check('asin','aas',text)
    Response = (text, 'https://www.amazon.com/Flash-Furniture-Nantucket-Umbrella-Folding/dp/B07CD5W2QC/ref=zg_bs_1613538101')
    if isinstance(text, str):
        # for i in spider.get_bsr_title(Response):
        #     print(i)
        print(spider.get_bsr_title(Response))
        # print(spider.get_detail_inf(Response))
        for i in spider.get_bsr_title(Response):
            print(i)




