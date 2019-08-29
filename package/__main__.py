# -*- coding: UTF-8 -*-

import sys
from flask import Flask, jsonify, request, Response
import time
from yf.ms import Ms
import re

from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/api/ping', methods=['GET'])
def ping():
    result = time.time()
    return jsonify(result)


@app.route('/api/microsoft/post', methods=['POST'])
def mic_request():
    # 检查参数是否包含 用户名、 密码、 全链接、 官网链接
    if request.values and 'UserName' in request.values and 'UserPass' in request.values \
            and 'FullUrl' in request.values and 'HeadUrl' in request.values:
        user_name = request.values['UserName']
        user_pass = request.values['UserPass']
        full_url = request.values['FullUrl']
        head_url = request.values['HeadUrl']
    else:
        return Response('parameter error', status=403)
    # 设置oauth2 授权网站及参数
    login_url = 'https://login.microsoftonline.com/extSTS.srf'
    login_data = '''<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"  
                      xmlns:a="http://www.w3.org/2005/08/addressing"  
                      xmlns:u="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <s:Header>
                        <a:Action s:mustUnderstand="1">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</a:Action>
                        <a:ReplyTo>
                            <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
                        </a:ReplyTo>
                        <a:To s:mustUnderstand="1">https://login.microsoftonline.com/extSTS.srf</a:To>
                        <o:Security s:mustUnderstand="1"  
                       xmlns:o="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                            <o:UsernameToken>
                                <o:Username>%s</o:Username>
                                <o:Password>%s</o:Password>
                            </o:UsernameToken>
                        </o:Security>
                    </s:Header>
                    <s:Body>
                        <t:RequestSecurityToken xmlns:t="http://schemas.xmlsoap.org/ws/2005/02/trust">
                            <wsp:AppliesTo xmlns:wsp="http://schemas.xmlsoap.org/ws/2004/09/policy">
                                <a:EndpointReference>
                                    <a:Address>%s</a:Address>
                                </a:EndpointReference>
                            </wsp:AppliesTo>
                            <t:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</t:KeyType>
                            <t:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</t:RequestType>
                            <t:TokenType>urn:oasis:names:tc:SAML:1.0:assertion</t:TokenType>
                        </t:RequestSecurityToken>
                    </s:Body>
                    </s:Envelope>'''
    # 实例化 授权类
    mm = Ms()
    # res = mm.opener_ms(login_url,
    #                    login_data % ('ibm.esb@yfsafety.com', 'Yfss@api2019', 'https://myyfai.sharepoint.com'))
    # 获取 token
    res = mm.opener_ms(login_url,
                       login_data % (user_name, user_pass, head_url))
    if res == '':
        return Response("Username or Password error, please check again!", status=403)
    # 匹配出授权后 token
    patten = re.compile('<wsse:BinarySecurityToken Id="Compact0" .*?">(.*?)</wsse:BinarySecurityToken>')
    li = re.findall(patten, res)
    if len(li) != 1:
        return Response("get token failure", status=403)

    # 根据请求网站url  拼接授权网站
    auth_url = head_url + '/_forms/default.aspx?wa=wsignin1.0'
    data1 = li[0]

    # 获取token 授权后的cookies
    res1 = mm.opener_ms(auth_url, data1)
    if res1 == '':
        return Response('', status=403)
    ms_cookies = list()

    # 在cookies中找出 rtFa 和FedAuth 关键字的值 用作后期授权访问使用
    for item in mm.cookie:
        if 'rtFa' == item.name:
            ms_cookies.append(item.name + '=' + item.value)
        if 'FedAuth' == item.name:
            ms_cookies.append(item.name + '=' + item.value)
    if len(ms_cookies) < 2:
        return Response("Cookies get Error", status=403)
    # full_url = 'https://myyfai.sharepoint.com/sites/projectsite-yfsafetydev/_api/projectdata/Projects'

    # 将rtFa 和FedAuth 做为header信息去请求自己要请求的网站
    res = mm.request_ms(full_url, ms_cookies)
    if res == "NO COOKIES":
        return Response("Username or Password error, please check again!", status=403)
    return Response(res, status=200)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    print("port is ", port)
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()

