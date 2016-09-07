import urllib2
import re
import time

def save_news(url,html):
#try:
#		response = urllib2.urlopen(url)
#	except urllib2.URLError, e:
#		print e.reason
#		return "ERROR"
#	html = response.read()

	# to get ID
	id_pattern = re.compile(r'thunews/.*?/.*?/.*?/')
	id_list = re.findall(id_pattern, url)
	news_id = id_list[0]
	list_ = re.split(re.compile(r'/'), news_id)
	news_id = list_[3]

	# file operation
	f = file('data/'+news_id+'.txt', "w")
	#print "ID:",news_id
	f.write(news_id+'\n');

	# to get news time
	time_pattern = re.compile(r'<div class="articletime">.*?</div>')
	time_list = re.findall(time_pattern, html)
	for time in time_list:
		actual_time = re.sub(re.compile(r'<.*?>'),'',time)
		if len(actual_time):
			#print 'TIME:',actual_time
			f.write(actual_time+'\n')
			break
	
	# to get title
	title_pattern = re.compile(r'<h1.*?/h1>')
	title_list = re.findall(title_pattern, html)
	for title in title_list:
		actual_title = re.sub(re.compile(r'<.*?>'),'',title)
		if len(actual_title):
			#print 'TITLE:', actual_title
#f.write(actual_title)
			break
		print '\n'
	
	# to get artical
	#print 'ARTICLE:'
	artical_pattern = re.compile(r'<article.*/article>',re.S)
	artical_list = re.findall(artical_pattern, html)
	for artical in artical_list:
		actual_artical = re.sub(re.compile(r'&.*?;'),'',artical)
		actual_artical = re.split(re.compile(r'<.*?>'),actual_artical)
		for paragraph in actual_artical:
			if len(paragraph):
				#print paragraph
				f.write(paragraph+'\n')
	f.close()
	return news_id

def get_urls(url_):
	pattern = re.compile(r'publish/thunews/.*?\.html')
	request = urllib2.Request(url_)
	try:
		response = urllib2.urlopen(request)
		#time.sleep(0.05)
	except urllib2.HTTPError, e:
		print e.code
		return []
	except urllib2.URLError, e:
		print e.reason
		return []
	list_ = re.findall(pattern, response.read())
	return list_

import Queue

initial_page = "http://news.tsinghua.edu.cn/publish/thunews/index.html"

url_queue = Queue.Queue()
seen = set()

seen.add(initial_page)
url_queue.put(initial_page)

cnt = 0 

f=file("urls.txt","w")

while (True):
	if url_queue.empty() == False:
		current_url = url_queue.get()

		news_pages = re.findall(re.compile(r'.*?_.html'),current_url);
		for news_page in news_pages:
			try:
				response = urllib2.urlopen(news_page)
				html = response.read()
			except urllib2.URLError, e:
				print e.reason
				continue

			cnt = cnt + 1
			f.write(news_page+' '+save_news(news_page,html)+'\n')
			print cnt, ':', news_page, 'size of queue:', url_queue.qsize(), "    size of set:", len(seen)

		#cnt = cnt + 1
		#f.write(current_url+'\n')
		#news_url = 
		#print cnt, ':', re.findall(re.compile(r'.*?_.html'),current_url)
		urls = get_urls(current_url)
		for next_url in urls:
			actual_url = "http://news.tsinghua.edu.cn/" + next_url
			if actual_url not in seen:
				seen.add(actual_url)
				url_queue.put(actual_url)
	else:
		break
