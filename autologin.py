#!/usr/bin/python3
#coding:utf-8

import urllib.request
import urllib.parse
import http.cookiejar
import smtplib

from email.mime.text import MIMEText
from email.header import Header

user = 'footoo.notifications@gmail.com'
passwd = '202,118,239,46'
to = 'cliffwoo@gmail.com'

def autologin(url, params, req_encoding, res_encoding):
	cookiejar = http.cookiejar.CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
	urllib.request.install_opener(opener)
	
	params = urllib.parse.urlencode(params)
	params = params.encode(req_encoding)
	response = urllib.request.urlopen(url, params)

	text = response.read()
	
	text_decode = text.decode(req_encoding)
	text = text_decode.encode(res_encoding)
	
	return text

def check(ip, passwd): 
	params = {"fr":"00", "id_ip":ip, "pass":passwd, "set":"进入"}
	req_encoding = 'gb2312'
	res_encoding = 'utf-8'
	text = autologin('http://hitsun.hit.edu.cn/index1.php', params, req_encoding, res_encoding)
	text = str(text, 'utf-8')
	search_text = '所剩余额'
	for line in text.splitlines():
		if line.find(search_text)!=-1:
			return(line.split(';')[2].split(' ')[0])

def genMail(iplist, user, to):
	context = ''
	for (ip,passwd) in iplist.items():
		context += ip + ": " + check(ip, passwd) + '\n'
	context += '\n'
	msg = MIMEText(context.encode('utf-8'), 'plain', 'utf-8')
	sub = Header('当月服务器余额情况', 'utf-8')
	msg['Subject'] = sub
	msg['From'] = user
	msg['To'] = to
	return msg

def sendMail(From, FromPass, To, mail):
	if not mail:
		return
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(From, FromPass)
	server.sendmail(From, To, mail)
	server.close()

if __name__ == '__main__':
	iplist = {	'202.118.239.46':'123456', 
				'202.118.250.18':'123456', 
				'202.118.250.19':'123456'}
	mail = genMail(iplist, user, to)
	sendMail(user, passwd, to, mail.as_string())

