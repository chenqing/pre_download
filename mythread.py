#!/usr/bin/python
#coding=utf-8
import threading
from Queue import Queue


class ThreadUrl(threading.Thread):
	'''
	封装多线程库，用来多线程跑啊
	'''

	def __init__(self,queue,site):
        	threading.Thread.__init__(self)
        	self.queue = queue
        	self.site = site  #传递的是一个class的实例或者引用

	def run(self):

		while True:
			try:
				uu = self.queue.get()
				t = self.site(uu)
			except:
				pass
			self.queue.task_done()



def mythread(urls,run,num=20):
	'''
	urls: url的列表
	num:  结合队列，跑多线程的抓取，默认线程数是20个
	run:  这个是threading之中run() 默认有一个参数，即urls中的元素 
	'''
	queue = Queue()

	for i in range(num):

		t= ThreadUrl(queue,run)

		t.setDaemon(True)

		t.start()


	for url in urls:

		queue.put(url)

        queue.join()

	

