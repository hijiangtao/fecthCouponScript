#coding=utf-8
import time
import httplib
import xlwt
from splinter import Browser

def splinter(url):
	browser = Browser('chrome')

	browser.visit(url.decode('utf-8', 'ignore'))
	#wait web element loading
	time.sleep(5)
	#fill in account and password
	browser.find_by_id('session_key-login').fill('')#fill in the login name here
	browser.find_by_id('session_password-login').fill('')#fill in the login password here
    #click the button of login
	browser.find_by_id('signin').click()
	#transfer to the search url

	n = 0
	col1_name = 'Name'
	col2_name = 'Job'
	col3_name = 'Place'
	col4_name = 'Link'
	book = xlwt.Workbook()

	sh = book.add_sheet("sheet 1")

	sh.write(n,0,"No")
	sh.write(n,1,col1_name)
	sh.write(n,2,col2_name)
	sh.write(n,3,col3_name)
	sh.write(n,4,col4_name)
	n += 1
	i = 0
	for i in range(0,80):
		#fetch the info of alumni of BIT from 1970s, 11028 is the school ID, you can customize it as you like
		link_url = 'http://www.linkedin.com/edu/alumni?id=11028&facets=&keyword=&dateType=attended&startYear=1970&endYear=2014&incNoDates=true&start=' + str(i*200) + '&count=200&filters=off&trk=edu-up-nav-menu-alumni' 
		browser.visit(link_url)
		time.sleep(5)

		contain = browser.find_by_id('my-feed-post')
		div_people = [div['id'] for div in contain.find_by_tag('div')]

		for each in div_people:
			if each != "":
				try:
					obj = browser.find_by_id(each).first
					job = obj.find_by_tag('p').first.value
					link = obj.find_by_tag('a').first['href']
					name = obj.find_by_tag('a').last['title']
					no = n
					place = obj.find_by_tag('p')[1].value
					sh.write(n,0,no)
					sh.write(n,4,link)
					sh.write(n,1,name)
					sh.write(n,2,job)
					sh.write(n,3,place)
					n+=1
				except each=="":
					print "Badway"
		book.save('result.xls')
	
	book.save('result.xls')
	
    
    # print urls
	browser.quit()

if __name__ == '__main__':
	websize3 ='https://www.linkedin.com/'
	splinter(websize3)