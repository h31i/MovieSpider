# coding:utf-8
import sys
import requests
import re
import json
from urllib import quote
from urllib import urlretrieve
import execjs
from bs4 import BeautifulSoup

'''
@url:http://api.xfsub.com/index.php?url=http://www.iqiyi.com/v_19rr0mx4z4.html
'''

class video_downloader(object):
	"""docstring for video_downloader"""
	def __init__(self, url):
		self.info = ""
		self.server = "http://api.xfsub.com"
		self.api = "http://api.xfsub.com/index.php?url="
		self.url = url.split('#')[0]
		self.target = self.api + self.url
		self.s = requests.session()

	def get_key(self):
		head = {
		'Referer': 'http://api.xfsub.com/index.php?url=http://www.iqiyi.com/v_19rr0mx4z4.html',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
		'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Host': 'api.177537.com',
		}
		req = self.s.get(url=self.target)
		req.encoding = 'utf-8'
		self.target = BeautifulSoup(req.text,'html.parser').iframe['src']
		req = self.s.get(self.target,headers=head)
		req.encoding = 'utf-8'

		raw_data = re.findall(r'"url.php", (.+),',req.text)[0]
		'''
		{
			"time":"1528986843",
			"key":"01d2cf374304b86b7e58e546c3e9f8a9",
			"url":"http://www.iqiyi.com/v_19rr0mx4z4.html",
			"type":"iqiyi",
			"ckey1":  encodeURIComponent(sign("http://www.iqiyi.com/v_19rr0mx4z4.html"))
		}		
		'''
		json_data = ','.join(raw_data.split(',')[:-1])+'}'

		self.info = json.loads(json_data)

		print self.info['url']

	def sign(self):
		with open("code.js") as f:
			js_data = execjs.compile(f.read())
		self.ckey = quote(js_data.call("sign",self.url))

	def get_url(self):

		#ckey = parse.quote(sign(self.info['url']))
		'''
		time=1528990613&
		key=a28713222e971129fc045ba26acd80fd&
		url=http%3A%2F%2Fwww.iqiyi.com%2Fv_19rr0mx4z4.html&
		type=iqiyi&
		ckey1=Mnit7CKjtYZNQB0Hzqzgh618CptPJOGPWmpxZJqs83BTU%252FBRA%252FNRarlD30GBuCgI
		'''
		real_url = "https://api.177537.com/url.php"
		header = {
			'Origin': 'https://api.177537.com',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'X-Requested-With': 'XMLHttpRequest',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
			'Host': 'api.177537.com',
		}

		data = {
			'time':self.info['time'],
			'key':self.info['key'],
			'url':self.info['url'],
			'type':self.info['type'],
			'ckey1':''
		}
		data['ckey1'] = self.ckey

		#'ckey1':ckey
		#'ckey1':encodeURIComponent(sign("http://www.iqiyi.com/v_19rr0mx4z4.html"))
		req = self.s.post(real_url,data=data)
		return json.loads(req.text)['url']

	def schedule(self,a,b,c):
		per = 100.0*a*b/c
		if per > 100:
			per = 1
		sys.stdout.write("	"+"%.2f%% have download:%ld file:%ld" % (per,a*b,c) + '\r')
		sys.stdout.flush()

	def video_download(self,url,filename):
		urlretrieve(url=url,filename=filename,reporthook=self.schedule)

if __name__ == '__main__':
	url = 'http://www.iqiyi.com/v_19rr0mx4z4.html#vfrm=2-4-0-1'
	vd = video_downloader(url)
	vd.get_key()
	vd.sign()
	v_url = vd.get_url()
	print 'Get URL successful!:%s' % v_url
	vd.video_download(v_url,'bear'+'.mp4')
	print '\nover!'