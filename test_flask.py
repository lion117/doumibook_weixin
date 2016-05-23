#!/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from wechat_sdk import WechatConf , WechatBasic
from wechat_sdk.exceptions import OfficialAPIError

import hashlib, urllib, urllib2, re, time, json
import xml.etree.ElementTree as ET


from private_const import APP_SECRET_KEY, DOUBAN_APIKEY



app = Flask(__name__)
app.debug = True
app.secret_key = APP_SECRET_KEY


conf = WechatConf(
    token='ngixpro',
    appid='wx38fb2e32db95d3be',
    appsecret='your_appsecret',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='NSPdPctnDzrXRfWr11zAo65xqsXx3ynR6xgyO3FflGg'  # 如果传入此值则必须保证同时传入 token, appid
)

menu_info = {
    'button': [
        {
            'type': 'click',
            'name': '今日歌曲',
            'key': 'V1001_TODAY_MUSIC'
        },
        {
            'type': 'click',
            'name': '歌手简介',
            'key': 'V1001_TODAY_SINGER'
        },
        {
            'name': '菜单',
            'sub_button': [
                {
                    'type': 'view',
                    'name': '搜索',
                    'url': 'http://www.soso.com/'
                },
                {
                    'type': 'view',
                    'name': '视频',
                    'url': 'http://v.qq.com/'
                },
                {
                    'type': 'click',
                    'name': '赞一下我们',
                    'key': 'V1001_GOOD'
                }
            ]
        }
    ]
}


py_wechat = WechatBasic(conf=conf)
try:
    py_wechat.create_menu(menu_info)
except OfficialAPIError , ex :
    print ex

#homepage just for fun
@app.route('/')
def home():
    return render_template('index.html')




#公众号消息服务器网址接入验证
#需要在公众帐号管理台手动提交, 验证后方可接收微信服务器的消息推送
@app.route('/weixin', methods=['GET'])
def weixin_access_verify():
    echostr = request.args.get('echostr')
    if verification(request) and echostr is not None:
        return echostr
    return 'access verification fail'




# 来自微信服务器的消息推送
@app.route('/weixin', methods=['POST'])
def weixin_msg():
    if verification(request):
        data = request.data
        py_wechat.parse_data(data)
        # 获得解析结果, message 为 WechatMessage 对象 (wechat_sdk.messages中定义)
        message = py_wechat.get_message()
        response = None
        if message.type == 'text':
            if message.content == 'wechat':
                response = py_wechat.response_text(u'^_^')
            elif message.content == u"新闻":
                response = respon_news()
            # elif message.content == u"menu":
            #     response = create_menu()

            else:
                response = py_wechat.response_text(u'文字')
        elif message.type == 'image':
            response = py_wechat.response_text(u'图片')
        else:
            response = py_wechat.response_text(u'未知')

        return  response



#接入和消息推送都需要做校验
def verification(request):
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    if py_wechat.check_signature(signature=signature , timestamp=timestamp ,nonce= nonce):
        return True
    return False



def respon_news():
    response = py_wechat.response_news([
        {
            'title': u'测试网页',
            'description': u'第一条新闻描述，这条新闻没有预览图',
            'url': u'http://www.google.com.hk/',
        }, {
            'title': u'文件1',
            'description': u'今天你吃饭了吗, 这是第一次打通为微信公众平台, 这是我需要尽快完成的工作',
            'picurl': u'http://www.diyifanwen.com/Files/BeyondPic/2008-10/20/08102023231459334.jpg',
            'url': u'http://www.github.com/',
        }, {
            'title': u'新闻2标题',
            'description': u'今天你吃饭了吗, 这是第一次打通为微信公众平台, 这是我需要尽快完成的工作',
            'picurl': u'http://www.diyifanwen.com/Files/BeyondPic/2008-10/20/0810202314086125.jpg',
            'url': u'http://bbs.jointforce.com/forum.php?mod=viewthread&tid=16623&extra=page%3D1',
        }
    ])

    return  response


def create_menu():
    resp = py_wechat.create_menu(menu_info)
    return resp



# #将消息解析为dict
# def parse_msg(rawmsgstr):
#     root = ET.fromstring(rawmsgstr)
#     msg = {}
#     for child in root:
#         msg[child.tag] = child.text
#     return msg
#
#
#
# def is_text_msg(msg):
#     return msg['MsgType'] == 'text'
#
# def user_subscribe_event(msg):
#     return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'
#


# HELP_INFO = \
# u"""
# 欢迎关注豆米查书^_^
#
# 直接发送书名、作者或ISBN号等关键字，即可查询书籍信息
#
# 如发送“东野圭吾”，将回复豆瓣查询到的三条数据记录
# """
#
# def help_info(msg):
#     return response_text_msg(msg, HELP_INFO)
#
#
#
# #访问豆瓣API获取书籍数据
# BOOK_URL_BASE = 'http://api.douban.com/v2/book/search'
# def search_book(q):
#     params = {'q': q.encode('utf-8'), 'apikey': DOUBAN_APIKEY, 'count': 3}
#     url = BOOK_URL_BASE + '?' + urllib.urlencode(params)
#     resp = urllib2.urlopen(url)
#     r = json.loads(resp.read())
#     books = r['books']
#     return books
#



# NEWS_MSG_HEADER_TPL = \
# u"""
# <xml>
# <ToUserName><![CDATA[%s]]></ToUserName>
# <FromUserName><![CDATA[%s]]></FromUserName>
# <CreateTime>%s</CreateTime>
# <MsgType><![CDATA[news]]></MsgType>
# <Content><![CDATA[]]></Content>
# <ArticleCount>%d</ArticleCount>
# <Articles>
# """
#
# NEWS_MSG_TAIL = \
# u"""
# </Articles>
# <FuncFlag>1</FuncFlag>
# </xml>
# """
#
# #消息回复，采用news图文消息格式
# def response_news_msg(recvmsg, books):
#     msgHeader = NEWS_MSG_HEADER_TPL % (recvmsg['FromUserName'], recvmsg['ToUserName'],
#         str(int(time.time())), len(books))
#     msg = ''
#     msg += msgHeader
#     msg += make_articles(books)
#     msg += NEWS_MSG_TAIL
#     return msg
#
# def make_articles(books):
#     msg = ''
#     if len(books) == 1:
#         msg += make_single_item(books[0])
#     else:
#         for i, book in enumerate(books):
#             msg += make_item(book, i+1)
#     return msg

# NEWS_MSG_ITEM_TPL = \
# u"""
# <item>
#     <Title><![CDATA[%s]]></Title>
#     <Description><![CDATA[%s]]></Description>
#     <PicUrl><![CDATA[%s]]></PicUrl>
#     <Url><![CDATA[%s]]></Url>
# </item>
# """
#
# def make_item(book, itemindex):
#     title = u'%s\t%s分\n%s\n%s\t%s' % (book['title'], book['rating']['average'],
#         ','.join(book['author']), book['publisher'], book['price'])
#     description = ''
#     picUrl = book['images']['large'] if itemindex == 1 else book['images']['small']
#     url = book['alt']
#     item = NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
#     return item
#
# #图文格式消息只有单独一条时，可以显示更多的description信息，所以单独处理
# def make_single_item(book):
#     title = u'%s\t%s分' % (book['title'], book['rating']['average'])
#     description = '%s\n%s\t%s' % (','.join(book['author']), book['publisher'], book['price'])
#     picUrl = book['images']['large']
#     url = book['alt']
#     item = NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
#     return item
#
# TEXT_MSG_TPL = \
# u"""
# <xml>
# <ToUserName><![CDATA[%s]]></ToUserName>
# <FromUserName><![CDATA[%s]]></FromUserName>
# <CreateTime>%s</CreateTime>
# <MsgType><![CDATA[text]]></MsgType>
# <Content><![CDATA[%s]]></Content>
# <FuncFlag>0</FuncFlag>
# </xml>
# """
#




# def response_text_msg(msg, content):
#     s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'],
#         str(int(time.time())), content)
#     return s


if __name__ == '__main__':
    app.run(host='localhost' , port=80)
