# -*- coding: utf-8 -*-
import sys
import requests
from urllib import request
from http import cookiejar
import re


class Ms(object):
    def __init__(self):
        self.cookie = cookiejar.CookieJar()
        # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        self.handler = request.HTTPCookieProcessor(self.cookie)
        # 通过CookieHandler创建opener
        self.opener = request.build_opener(self.handler)
        self.header = {
            'Content-Type': 'text/xml',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
        }

    def reload_opener(self):
        self.handler = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.handler)

    def opener_ms(self, url, data):
        postdata = data.encode('UTF8')
        req = request.Request(url, postdata, self.header)
        # for item in self.cookie:
        #     print("cookie name = ", item.name)
        # 此处的open方法打开网页
        response = self.opener.open(req)
        if response.code == 200:
            res = response.read()
            return str(res)
        return ''

    def request_ms(self, url, ms_cookies):
        if len(ms_cookies) < 2:
            return "NO COOKIES"
        header = {
            'Content-Type': 'text/xml',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
            'Cookie': ms_cookies[0] + ';' + ms_cookies[1]}
        # print('header ', header)
        wbdata = requests.get(url, headers=header).text
        return wbdata

    # def list2str(self,cookies):
    #     result = ''
    #     for l in cookies:
    #         if '' == result
    #         result = result + l

#
# if __name__ == '__main__':
#     print("HI")
#     url = 'https://login.microsoftonline.com/extSTS.srf'
#     data = '''<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
#                   xmlns:a="http://www.w3.org/2005/08/addressing"
#                   xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
#                 <s:Header>
#                     <a:Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</a:Action>
#                     <a:ReplyTo>
#                         <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
#                     </a:ReplyTo>
#                     <a:To s:mustUnderstand="1">https://login.microsoftonline.com/extSTS.srf</a:To>
#                     <o:Security s:mustUnderstand="1"
#                    xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
#                         <o:UsernameToken>
#                             <o:Username>%s</o:Username>
#                             <o:Password>%s</o:Password>
#                         </o:UsernameToken>
#                     </o:Security>
#                 </s:Header>
#                 <s:Body>
#                     <t:RequestSecurityToken xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust">
#                         <wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy">
#                             <a:EndpointReference>
#                                 <a:Address>%s</a:Address>
#                             </a:EndpointReference>
#                         </wsp:AppliesTo>
#                         <t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType>
#                         <t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType>
#                         <t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType>
#                     </t:RequestSecurityToken>
#                 </s:Body>
#                 </s:Envelope>'''
#     ms = Ms()
#     res = ms.opener_ms(url, data % ('ibm.esb@yfsafety.com', 'Yfss@api2019', 'https://myyfai.sharepoint.com'))
#     print(res)
#     patten = re.compile('<wsse:BinarySecurityToken Id="Compact0" .*?">(.*?)</wsse:BinarySecurityToken>')
#     li = re.findall(patten, res)
#     print(li)
#     if len(li) != 1:
#         sys.exit(1)
#     url1 = 'https://myyfai.sharepoint.com/_forms/default.aspx?wa=wsignin1.0'
#     data1 = li[0]
#     res1 = ms.opener_ms(url1, data1)
#     ms_cookies = list();
#     for item in ms.cookie:
#         if 'rtFa' == item.name:
#             ms_cookies.append(item.name + '=' + item.value)
#         if 'FedAuth' == item.name:
#             ms_cookies.append(item.name + '=' + item.value)
#     if len(ms_cookies) < 2:
#         sys.exit(1)
#     print(ms_cookies)
#     url2 = 'https://myyfai.sharepoint.com/sites/projectsite-yfsafetydev/_api/projectdata/Projects'
#     res = ms.request_ms(url2, ms_cookies)
#     print(res)

