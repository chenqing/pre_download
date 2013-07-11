#!/usr/bin/env python
#coding=utf-8
from urllib2 import urlopen,ProxyHandler,install_opener,build_opener
from bs4 import BeautifulSoup
import sys
import re
import chardet
import codecs
import urllib
import mythread

'''
	用法 python pre_down.py  www.qq.com  proxy_ip
'''

urls = [] 

def extract_css(css_url):
	'''
		解析css文件里面的图片链接等
	'''
	line = urlopen(css_url).read()
	
	for l in  re.findall(r'url\((.*?)\)',line):
		if l.startswith('http://') :
			urls.append(l)


def image_url(res,line):
	'''
		挑选图片，包括从css中，或者页面中
	'''

	for l in res.findall(line):
		urls.append(l)

def extract_url(domain):
	'''
		 将domain 首页里面所有的url进行提取，提取出所有的链接，放到urls
	'''
	

	line = urllib.urlopen(domain).read()
		
	data = BeautifulSoup(line)
	links = data.findAll('a')
	for a in links:
		try:
			if a.has_attr('href'):
				if a['href'].startswith('http://'):
					urls.append(a['href'])
				if a['href'].endswith('.css'):
					extract_css(a['href'])
		except:
			print 'some error heppend'
	#以下获取src的连接
	try:
		src = re.findall(r'src="(.*?)"',line)
		for url in src:
			if url.endswith('.css'):
				extract_css(url)
			else:
				urls.append(url)
			
	except:
		pass


	#以下获取url() 中的链接
	try:
		url = re.findall(r'url\((.*?)\)',line)
		for u in url:
			if u.startswith('http://'):
				urls.append(u)
	except:
		pass		

def pre_down(url):
	'''
		将url，通过设置代理进行预加载下来
	'''
	proxy = ProxyHandler({'http':'http://'+proxy_ip+':80'})
	opener = build_opener(proxy)
	install_opener(opener)
	try:
		urlopen(url)
		print '%s 下载好了 ' %(url)
	except:
		pass

if __name__ == '__main__':
	domain = ''
	proxy_ip = ''
	if len(sys.argv) > 2:
		domain = sys.argv[1]
		proxy_ip = sys.argv[2]
	else:
		print ' Useage: python  %s  domain  proxy_ip ' %(sys.argv[0])
		print ' Example:  python  pre_down.py www.sina.com.cn  221.130.162.34'
		sys.exit(1)

	if not domain.startswith('http://'):
		domain = 'http://' + domain
	
	extract_url(domain)	

	ok = []

	for url in urls:
		if url.startswith('http:'):
			ok.append(url)
	mythread.mythread(list(set(ok)),pre_down,40)

			
