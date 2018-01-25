# -*- coding:utf-8 -*-
"""
File Name: utils
Version:
Description:
Author: liuxuewen
Date: 2017/5/19 10:24
"""
import time
import os
import sys
import random
import requests
import redis
from aws_proxies import get_proxies
from redis_bf import BloomFilter
from multiprocessing import Lock
from comm_log import comm_log

reload(sys)
sys.setdefaultencoding("utf-8")

lock=Lock()
sess=requests.session()
sess.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
logger=comm_log(111)
#roxies=['http://54.222.232.0:3128', 'http://116.248.63.95:8998', 'http://162.243.18.46:3128','http://27.213.44.204:8998', 'http://61.160.233.8:8080','http://117.54.120.20:3129','http://12.181.44.68:8008','http://125.93.149.47:9000']
#图片去重
bf = BloomFilter(block_num=2, key="gengmei")

def check_path(path):
    '''
    检查照片存储路径是否已存在，不存在则新建
    :param self: 
    :param path: 
    :return: 
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def reque(url):
    """
    请求超时，再次发起请求
    :param sess: 
    :param url: 
    :return: 
    """
    times = 1
    while times < 5:
        try:
            sess.proxies = get_proxies()
            res = sess.get(url, timeout=3)
            return res
        except Exception as e:
            #logger.warning(str(e))
            time.sleep(random.random())
            times += 1
    logger.info(u'请求失败：{}'.format(url))
    return None


def save_img(urls, path):
    '''
    保存图片
    :param sess: 
    :param urls: 
    :param path: 
    :return: 
    '''
    nums = len(os.listdir(path))
    for i, url in enumerate(urls):
        lock.acquire()
        if not bf.check_in(url):
            res = reque(url)
            if res:
                with open('{}/{}.jpg'.format(path, nums + i), 'wb') as f:
                    f.write(res.content)
                    bf.insert(url)
            else:
                logger.info(u"无法下载图片：{}".format(url))
            time.sleep(3 * random.random())
        lock.release()


def split_urls(urls):
    k = len(urls) / 12
    if k > 1:
        return urls[:k], urls[k:2 * k], urls[2 * k:3 * k], urls[3 * k:4 * k], urls[4 * k:5 * k],urls[5 * k:6 * k], urls[6 * k:7 * k], urls[7 * k:8 * k], urls[8 * k:9 * k], urls[9 * k:10*k],urls[10 * k:11 * k], urls[11 * k:]
        #return urls[:k], urls[k:2 * k], urls[2 * k:3 * k], urls[3 * k:4 * k], urls[4 * k:]
    else:
        return urls,

