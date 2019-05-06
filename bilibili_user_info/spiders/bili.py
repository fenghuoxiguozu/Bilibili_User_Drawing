# -*- coding: utf-8 -*-
import scrapy
import math
import json
from scrapy.spiders import Spider
from bilibili_user_info.items import BilibiliUserInfoItem
from scrapy_redis.spiders import RedisSpider

# item = BilibiliUserInfoItem()
class BiliSpider(RedisSpider):
    name = 'bili'
    allowed_domains = ['bilibili.com']
    reids_keys = 'bilibili:start_urls'

# lpush bilibili:start_urls https://api.bilibili.com/x/relation/followers?vmid=68565807&pn=1&ps=20&order=desc
#     start_urls = ['https://api.bilibili.com/x/relation/followers?vmid=68565807&pn=1&ps=20&order=desc']
    first_urls ='https://api.bilibili.com/x/relation/followers?vmid=68565807&pn={}&ps=20&order=desc'
    base_medialist_url='https://api.bilibili.com/x/space/fav/nav?mid={}&jsonp=jsonp'
    base_love_url='https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id={}&pn={}&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'

#user_mid 获取用户URL
    def parse(self, response):
        # item=BilibiliUserInfoItem()
        json_data=json.loads(response.text)
        fans_num=json_data['data']['total']
        # page=math.ceil(fans_num/20)
        users=json_data['data']['list']
        for user in users:
            user_mid = user['mid']
            user_uname = user['uname']
            media_url=self.base_medialist_url.format(user_mid)
            follow_user='https://api.bilibili.com/x/relation/followers?vmid={}&pn=1&ps=20&order=desc'.format(user_mid)
            if fans_num>0:  #判断是否有粉丝数
                yield scrapy.Request(url=follow_user,callback=self.parse)
            yield scrapy.Request(url=media_url,callback=self.parse_user,meta={'user_mid':user_mid,'user_uname':user_uname})

        for i in range(2,6):  #限制只访问前5页
            next_url=self.first_urls.format(i)
            yield scrapy.Request(url=next_url,callback=self.parse)

#收藏视频列表
    def parse_user(self,response):
        user_mid=response.meta['user_mid']
        user_uname=response.meta['user_uname']
        json_data=json.loads(response.text)
        media_data = json_data['data']['archive']
        media_list=[]
        for i in media_data:
            media_list.append(i['media_id'])
        if len(media_list)>0:
            for  media_id in media_list:
                love_url=self.base_love_url.format(media_id,1)
                yield scrapy.Request(url=love_url,callback=self.parse_love_page,meta={'media_id':media_id,'user_mid':user_mid,'user_uname':user_uname})

#收藏视频所有页数URL
    def parse_love_page(self,response):
        user_mid = response.meta['user_mid']
        user_uname = response.meta['user_uname']
        media_id = response.meta['media_id']
        json_data = json.loads(response.text)
        movies_num = json_data['data']['info']['media_count']
        movies_page = math.ceil(int(movies_num)/20)
        if movies_num > 0:  # 判断是否有收藏的视频
            # if movies_page>1:
            for i in range(0,movies_page+1):
                next_love_url= self.base_love_url.format(media_id, i)
                yield scrapy.Request(url=next_love_url,callback=self.parse_love,meta={'user_mid':user_mid,'user_uname':user_uname})

    def parse_love(self, response):
        item = BilibiliUserInfoItem()
        item['user_mid'] = response.meta['user_mid']
        item['user_uname'] = response.meta['user_uname']
        # item['user_url'] = 'https://space.bilibili.com/{}/favlist'.format(user_mid)

        movies = []
        json_data = json.loads(response.text)
        datas = json_data['data']['medias']
        for data in datas:
            movie=data['title']
            movies.append(movie)

        item['movies'] = movies
        yield item




