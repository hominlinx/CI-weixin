# coding: UTF-8
import urllib2,cookielib,re
import json
import hashlib
from urllib import URLopener

'''
    author:hominlinx
    version:1.0
    datetime:2013-8-28
    email:hominlinx@gmail.com
'''
def goodboy(funcname): print "%s finished." % funcname

class WXSender:
    
    '''
		Using CI-weixin
    '''
    
    wx_cookie = ''      
    token = ''
    user_fakeid = ''    # 微信公众账号 fakeid
    friend_info = []        # 好友 fakeid
    
#     def __init__(self):
#         pass
        
    def login(self,account,pwd):
        # 获取 cookie
        cookies = cookielib.LWPCookieJar()
        cookie_support= urllib2.HTTPCookieProcessor(cookies)
        
        # bulid a new opener
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        
        pwd = hashlib.md5(pwd).hexdigest()
        req = urllib2.Request(url = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN',
                              data = ('username=' + account + 
                              '&pwd=' + pwd + 
                              '&imgcode='
                              '&f=json'))
        
        req.add_header("x-requested-with", "XMLHttpRequest")
        #req.add_header("referer", "https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN")
        req.add_header("referer", "https://mp.weixin.qq.com/")
        respond = opener.open(req).read()
        
        respond_json = json.loads(respond)
        
        if respond_json['ErrCode'] < 0:
            raise Exception("Login error.")
        
        s = re.search(r'token=(\d+)', respond_json['ErrMsg'])
        
        if not s:
            raise Exception("Login error.")
        
        self.token = s.group(1)
        
        for cookie in cookies:
            self.wx_cookie += cookie.name + '=' + cookie.value + ';'
#         print 'wx_cookie ',self.wx_cookie
#         print 'token ',self.token
        
        goodboy(self.login.__name__)
        
    def get_fakeid(self):
        if not (self.wx_cookie and self.token):
            raise Exception("Cookies or token is missing.")
        
        url = 'https://mp.weixin.qq.com/cgi-bin/userinfopage?t=wxm-setting&token=' + self.token + '&lang=zh_CN'
        req = urllib2.Request(url)
        req.add_header('cookie',self.wx_cookie)
        
        data = urllib2.urlopen(req,timeout = 4).read()
        
        m = re.search(r'fakeid = "(\d+)"',data,re.S | re.I)
        
        # group(0) == [fakeid = "123456789"]
        if not m:
            raise Exception("Getting fakeid failed.")
        
        self.user_fakeid = m.group(1)
        
        goodboy(self.get_fakeid.__name__)
        
    def get_friend_fakeid(self):
        if not (self.wx_cookie and self.token and self.user_fakeid):
            raise Exception("Cookies,token or user_fakeid is missing.")
        
        # 获取 friend fakeid
        base_url = ('https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&lang=zh_CN&pagesize=50' + 
                    '&type=0&groupid=0' + 
                    '&token=' + self.token + 
                    '&pageidx=')    # pageidx = ?
        
        #https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&token=941478109&lang=zh_CN&pagesize=10&pageidx=0&type=0&groupid=0
         #https://mp.weixin.qq.com/cgi-bin/contactmanage?t=user/index&lang=zh_CN&pagesize=50&type=0&groupid=0&token=941478109&pageidx=0
        
        # 这里可以根据微信好友的数量调整，由 base_url 可知一页可以显示 pagesize = 50 人，看实际情况吧。
        for page_idx in xrange(0,1000):
            url = base_url + str(page_idx)
            req = urllib2.Request(url)
            req.add_header('cookie',self.wx_cookie)
          
            #req.add_header("referer", "https://mp.weixin.qq.com/cgi-bin/userinfopage?t=wxm-setting&token=941478109&lang=zh_CN")
            data = urllib2.urlopen(req).read()
            p = re.compile(r'"id":([0-9]{4,20})')
            res = p.findall(data)
            if not res:
                break  
            
            for id in res:
                self.friend_info.append({"id":id})
                
        goodboy(self.get_friend_fakeid.__name__)
        
    def sender_fakeid(self,fakeid,msg = "Hello World."):
        if not (self.wx_cookie and self.token and self.user_fakeid and self.friend_info):
            raise Exception("Cookies,token,user_fakeid or friend_info is missing.")
        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&lang=zh_CN'
        post_data = ('type=1&content=%s&error=false&imgcode='
             '&token=%s'
             '&ajax=1&tofakeid=') % (msg,self.token)   # fakeid = ?
        fromfakeid = self.user_fakeid
        postdata = (post_data + fakeid).encode('utf-8')
        #print postdata

        req = urllib2.Request(url,postdata)
        req.add_header('cookie',self.wx_cookie)
        req.add_header('referer', ('https://mp.weixin.qq.com/cgi-bin/singlemsgpage?'
                                   'token=%s&fromfakeid=%s'
                                   '&msgid=&source=&count=20&t=wxm-singlechat&lang=zh_CN') % (self.token,fromfakeid))
            
        # {"ret":"0", "msg":"ok"}
        res = urllib2.urlopen(req).read()
        res_json = json.loads(res)
            
        if res_json["ret"] != "0":

           # do something.
           pass
            
        goodboy(self.get_friend_fakeid.__name__)

    def group_sender(self,msg = "Hello World."):
        if not (self.wx_cookie and self.token and self.user_fakeid and self.friend_info):
            raise Exception("Cookies,token,user_fakeid or friend_info is missing.")
        
        '''
        fakeId nickName groupId remarkName
        '''
        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&lang=zh_CN'
        post_data = ('type=1&content=%s&error=false&imgcode='
             '&token=%s'
             '&ajax=1&tofakeid=') % (msg,self.token)   # fakeid = ?
             
        fromfakeid = self.user_fakeid
        
        for friend in self.friend_info:
            postdata = (post_data + friend["id"]).encode('utf-8')
            
            #print postdata
            req = urllib2.Request(url,postdata)
            req.add_header('cookie',self.wx_cookie)
            
            # 添加 HTTP header 里的 referer 欺骗腾讯服务器。如果没有此 HTTP header，将得到登录超时的错误。
            req.add_header('referer', ('https://mp.weixin.qq.com/cgi-bin/singlemsgpage?'
                                   'token=%s&fromfakeid=%s'
                                   '&msgid=&source=&count=20&t=wxm-singlechat&lang=zh_CN') % (self.token,fromfakeid))
            
            # {"ret":"0", "msg":"ok"}
            res = urllib2.urlopen(req).read()
            res_json = json.loads(res)
            
            if res_json["ret"] != "0":
                # do something.
                pass
            
        goodboy(self.get_friend_fakeid.__name__)
    
    def run_test(self,account,pwd):
        # 登录，需要提供正确的账号密码
        self.login(account, pwd)
        
        # 获取微信公众账号 fakeid
        self.get_fakeid()
        
        # 获取微信好友的所有 fakeid，保存再 self.friend_info 中
        self.get_friend_fakeid()
        
        # 群发接口：目前只能发送文本信息
        #self.group_sender("test")
        self.sender_fakeid("2201337020","testh")
        
from urllib2 import BaseHandler, build_opener
class HTTPHeaderPrint(BaseHandler):
    def __init__(self):
        pass
    
    def http_request(self, request):
        print request.headers
        return request

    def http_response(self, request, response):
        print response.info()
        return response

    https_request = http_request
    https_response = http_response

if __name__ == '__main__':
    wxs = WXSender()
    #wxs.run_test("abc@abc.com","abc")
    wxs.run_test("gaosibei@126.com","244168abc")
    #wxs.run_test("daoluanxiaozi@126.com","a123456")
    
