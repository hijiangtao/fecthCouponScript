#coding=utf-8
import time
import httplib
import xlwt
import xlrd
import csv
import codecs
import os, urllib2, urllib
from splinter import Browser
from lxml import etree
import BeautifulSoup
import sys

#to ensure the right coding of the data
reload(sys)
sys.setdefaultencoding( "utf-8" )

#to read the first sheet of firneds list
def open_file(path):
	try:
		book = xlrd.open_workbook(path)
	except Exception, e:
		print "[Error]%s" % e

	try:
		first_sheet = book.sheet_by_index(0)
		links = first_sheet.col_values(4)
		ids = first_sheet.col_values(0)
	except Exception, e:
		print "[Error]%s" % e

	return (links, ids)

def read_singlepage(file):
	browser = Browser('chrome')
	url = 'https://www.linkedin.com/'
	browser.visit(url.decode('utf-8', 'ignore'))
	#wait web element loading
	time.sleep(0.5)

	f = open('./test.txt','a')
	
	#useful
	browser.find_by_id('session_key-login').fill('script@linkedin.com')#login name
	browser.find_by_id('session_password-login').fill('password')#password
	
	#click the button of login
	browser.find_by_id('signin').click()
	
	#open the file and read the links
	links, ids = open_file(file)
	data = map(lambda a,b:(a,b), links, ids)

	col_count = 0
	global col_name, col_val
	col_name = col_val = ['']
	col_name += [''] * 116
	col_val += [''] * 116
	book = xlwt.Workbook()
	
	#sketch data begin
	sh = book.add_sheet("detail")

	#base info 1-7
	col_name[0] = "id"
	col_name[1] = "name"
	col_name[2] = "headline"
	col_name[3] = "location_locality"
	col_name[4] = "location_industry"
	col_name[5] = "overview_summary_current"
	col_name[6] = "overview_summary_education"
	col_name[7] = "profile_link"

	#store the col_name of experience 8-31
	for i in range(0,6):
		col_name[i*4+8] = "exp_title_" + str(i+1)
		col_name[i*4+9] = "exp_company_" + str(i+1)
		col_name[i*4+10] = "exp_start_time_" + str(i+1)
		col_name[i*4+11] = "exp_stop_time_" + str(i+1)

	#store the col_name of skills 32-41
	for i in range(32,42):
		col_name[i] = "ski_detail_" + str(i-31)
	
	#store the col_name of education 42-59
	for i in range(0,3):
		temp = 42
		col_name[i*6 + temp] = "edu_title_" + str(i+1)
		temp += 1
		col_name[i*6 + temp] = "edu_degree_" + str(i+1)
		temp += 1
		col_name[i*6 + temp] = "edu_major_" + str(i+1)
		temp += 1
		col_name[i*6 + temp] = "edu_start_time_" + str(i+1)
		temp += 1
		col_name[i*6 + temp] = "edu_stop_time_" + str(i+1)
		temp += 1
		col_name[i*6 + temp] = "edu_detail_" + str(i+1)

	#store the col_name of honor 60-74
	for i in range(0,5):
		temp = 60
		col_name[i*3 + temp] = "ho_title_" + str(i+1)
		temp += 1
		col_name[i*3 + temp] = "ho_time_" + str(i+1)
		temp += 1
		col_name[i*3 + temp] = "ho_detail_" + str(i+1)

	#store the col_name of volunteer 75-99
	for i in range(0,5):
		temp = 75
		col_name[i*5 + temp] = "vol_title_" + str(i+1)
		temp += 1
		col_name[i*5 + temp] = "vol_org_" + str(i+1)
		temp += 1
		col_name[i*5 + temp] = "vol_time_" + str(i+1)
		temp += 1
		col_name[i*5 + temp] = "vol_locality_" + str(i+1)
		temp += 1
		col_name[i*5 + temp] = "vol_content_" + str(i+1)

	#store the col_name of interests 100
	col_name[100] = "interest_view"

	#store the col_name of lang 101-103
	for i in range(0,3):
		temp = 101
		col_name[i + temp] = "lang_section_" + str(i+1)

	#store the col_name of friends 104-115
	for i in range(0,6):
		temp = 104
		col_name[i*2 + temp] = "friend_name_" + str(i+1)
		temp += 1
		col_name[i*2 + temp] = "friend_link_" + str(i+1)

	for i in range(0,116):
		try:
			sh.write(col_count,i,col_name[i])
		except Exception, e:
			print "[Error]Problem %s" % e

	col_count += 1

	path = './'
	book.save('linkedin.xls')

	test = 0

	# do the stragety for each people
	for (slink, sid) in data:
		#get the screenshot of the people's CV
		
		if sid == 10721:
			test = 1
		
		if sid == 11000:
			break
		if test == 0:
			continue
		
		profile_name= str(sid) + ".jpg"
		dest_dir=os.path.join(path, profile_name)
		col_val[0] = sid
		# print slink
		browser.visit(slink)
		
		if browser.find_by_id('verification-code'):
			break
			
		#second login when the page shows fault in user's login state
		if browser.find_by_id('btn-primary'):
			browser.find_by_id('session_key-login').fill('script@linkedin.com')#login name
			browser.find_by_id('session_password-login').fill('password')#password
			browser.find_by_id('btn-primary').click()
		
		#end the process when the account is denied by linkedin official
		if not(browser.find_by_id('name')):
			if browser.find_by_id('verification-code'):
				break
			else:
				continue
			
		time.sleep(0.5)

		#get the first column data of LinkedIn
		try:
			col_val[1] = name = browser.find_by_id('name').find_by_tag('span').first.find_by_tag('span').first.value
			col_val[2] = headline = browser.find_by_id('headline').find_by_tag('p').value
			col_val[3] = location_locality = browser.find_by_id('location').find_by_tag('a').first.value
			col_val[4] = location_industry = browser.find_by_id('location').find_by_tag('a')[1].value
			col_val[5] = overview_summary_current = browser.find_by_id('overview-summary-current').find_by_tag('td').first.find_by_tag('a').value
			col_val[6] = overview_summary_education = browser.find_by_id('overview-summary-education').find_by_tag('td').first.find_by_tag('a').value
			col_val[7] = profile_link = browser.find_by_xpath('//*[@id="top-card"]/div/div[2]/div/ul/li/dl/dd/a')['href']
			
			content = u"NAME: " + name + u"\nHADLINE: " + headline + u"\nLOCATION_LOCALITY: " + location_locality + u"\nLOCATION_INDUSTRY: " + location_industry + u"\nOVERVIEW_SUMMARY_CURRENT: " + overview_summary_current + u"\nOVERVIEW_SUMMARY_EDUCATION: " + overview_summary_education + u"\nPROFILE_LINK: " + profile_link + u"\n"
			f.write(content)

		except Exception, e:
			print "[Error]The profile Info's getting some problems because of: %s" % e
		
		#get the background of details
		global background_experience, skills, background_education, background_honor, background_volunteer, div_exp, li_skill, div_edu, div_honor, div_vol
		global exp_title, exp_company, exp_start_time,exp_stop_time, ski_detail, edu_title, edu_degree, edu_title, edu_major, edu_detail, edu_start_time, edu_stop_time, ho_title, ho_time, ho_detail, vol_title, vol_org, vol_time, vol_locality, vol_content, lang_section, friend_name, friend_link
		exp_title = ['']*6; exp_company = ['']*6; exp_start_time = ['']*6; exp_stop_time = ['']*6; ski_detail = ['']*10; edu_title = ['']*3; edu_degree = ['']*3; edu_title = ['']*3; edu_major = ['']*3; edu_detail = ['']*3; edu_start_time = ['']*3; edu_stop_time = ['']*3; ho_title = ['']*5; ho_time = ['']*5; ho_detail = ['']*5; vol_title = ['']*5; vol_org = ['']*5; vol_time = ['']*5; vol_locality = ['']*5; vol_content = ['']*5; lang_section = ['']*3; friend_name = ['']*6; friend_link = ['']*6

		try:
			#i is used to count the experience of the people
			background_experience = browser.find_by_id('background-experience')
			div_exp = [div['id'] for div in background_experience.find_by_xpath('div')]

			i = 0
			for each in div_exp:
				if i <= 5:
					trans = browser.find_by_id(each).first

					exp_title[i] = trans.find_by_xpath('div/header/h4/a').first.value

					temp = trans.find_by_xpath('div/header/h5[2]/span/strong/a')
					if temp:
						exp_company[i] = temp.first.value
					elif trans.find_by_xpath('div/header/h5/a'):
						exp_company[i] = trans.find_by_xpath('div/header/h5/a').first.value
					else:
						exp_company[i] = trans.find_by_xpath('div/header/h5/span/strong/a').first.value

					exp_start_time[i] = trans.find_by_xpath('div/span/time').first.value
					exp_stop_time[i] = trans.find_by_xpath('div/span').first.value
					i += 1

					content = u"EXP_TITLE[%d]: %s\n" % (i-1, exp_title[i-1]) + u"EXP_COMPANY[%d]: %s\n" % (i-1, exp_company[i-1]) + u"EXP_START_TIME[%d]: %s\n" % (i-1, exp_start_time[i-1]) + u"EXP_STOP_TIME[%d]: %s" % (i-1, exp_stop_time[i-1]) + u"\n"
					print content
					f.write(content)
				else:
					break

		except Exception, e:
			print "[Error]Experience: %s" % e

		for i in range(0,6):
			col_val[i*4+8] = exp_title[i]
			col_val[i*4+9] = exp_company[i]
			col_val[i*4+10] = exp_start_time[i]
			col_val[i*4+11] = exp_stop_time[i]

		try:
			#j is used to count the skills of the people
			skills = browser.find_by_id('profile-skills')
			li_skill = [li for li in skills.find_by_xpath('ul/li')]

			j = 0
			for each in li_skill:
				temp = each.find_by_xpath('span/span/span')
				if j <= 9 and temp:
					ski_detail[j] = each.find_by_xpath('span/span/span').first.value
					
					content = u"SKI_DETAIL[%d]: %s\n" % (j, ski_detail[j])
					f.write(content)
					
					j += 1
				else:
					break

		except Exception, e:
			print "[Error]Skills: %s" % e

		for i in range(0,10):
			col_val[i+32] = ski_detail[i]

		try:
			#k is used to count the edu info
			background_education = browser.find_by_id('background-education')
			div_edu = [div for div in background_education.find_by_xpath('div')]

			k = 0

			for each in div_edu:
				if k <= 2:
					try:
						temp = each.find_by_xpath('div/div/header/h4/a')
						if temp:
							edu_title[k] = temp.first.value

						temp = each.find_by_xpath('div/div/header/h5/span[1]')
						if temp:
							edu_degree[k] = temp.text

						temp = each.find_by_xpath('div/div/header/h5/span[2]/a')
						if temp:
							edu_major[k] = temp.first.value

						temp = each.find_by_xpath('div/div/span/time[1]')
						if temp:
							edu_start_time[k] = temp.text

						temp = each.find_by_xpath('div/div/span/time[2]')
						if temp:
							edu_stop_time[k] = temp.text

						temp = each.find_by_xpath('div/div/p')
						if temp:
							edu_detail[k] = temp.first.value
						k += 1
						
						content = u"EDU_TITLE[%d]: %s\n" % (k-1, edu_title[k-1]) + u"EDU_DEGREE[%d]: %s\n" % (k-1, edu_degree[k-1])+ u"EDU_MAJOR[%d]: %s\n" % (k-1, edu_major[k-1]) + u"EDU_START_TIME[%d]: %s\n" % (k-1, edu_start_time[k-1]) + u"EDU_STOP_TIME[%d]: %s\n" % (k-1, edu_stop_time[k-1]) + u"EDU_DETAIL[%d]: %s\n" % (k-1, edu_detail[k-1])
						print content
						f.write(content)
					except Exception, e:
						print "[Error]Edu info each: %s" % e
				else:
					break

		except Exception, e:
			print "[Error]Edu Info: %s" % e

		for i in range(0,3):
			temp = 42
			col_val[i*6 + temp] = edu_title[i]
			temp += 1
			col_val[i*6 + temp] = edu_degree[i]
			temp += 1
			col_val[i*6 + temp] = edu_major[i]
			temp += 1
			col_val[i*6 + temp] = edu_start_time[i]
			temp += 1
			col_val[i*6 + temp] = edu_stop_time[i]
			temp += 1
			col_val[i*6 + temp] = edu_detail[i]

		try:
			#l
			background_honor = browser.find_by_id('background-honors')
			div_honor = [div for div in background_honor.find_by_xpath('div')]

			l = 0
			for each in div_honor:
				if l <= 4:
					try:
						temp = each.find_by_xpath('div/div/h4')
						if temp:
							ho_title[l] = each.find_by_xpath('div/div/h4/span[1]').text

						temp = each.find_by_xpath('div/div/span/time')
						if temp:
							ho_time[l] = temp.first.text

						temp = each.find_by_xpath('div/div/p')
						if temp:
							ho_detail[l] = temp.first.text
						
						l += 1
						content = u"HO_TITLE[%d]: %s\n" % (l-1, ho_title[l-1]) + u"HO_TIME[%d]: %s\n" % (l-1, ho_time[l-1]) + u"HO_DETAIL[%d]: %s\n" % (l-1, ho_detail[l-1])
						f.write(content) 
					except Exception, e:
						print "[Error]Honor Each: %s" % e
				else:
					break

		except Exception, e:
			print "[Error]Honor: %s" % e

		for i in range(0,5):
			temp = 60
			col_val[i*3 + temp] = ho_title[i]
			temp += 1
			col_val[i*3 + temp] = ho_time[i]
			temp += 1
			col_val[i*3 + temp] = ho_detail[i]

		try:
			#m
			background_volunteer = browser.find_by_id('background-volunteering')
			div_vol = [div for div in background_volunteer.find_by_xpath('div')]

			m = 0
			for each in div_vol:
				if (m <= 4) and (each):
					try:
						temp = each.find_by_xpath('div/div/hgroup/h4/span')
						if temp:
							vol_title[m] = temp.first.value

						temp = each.find_by_xpath('div/div/hgroup/h5[2]/a')
						if temp:
							vol_org[m] = temp.first.value 
						if each.find_by_xpath('div/div/span/time'):
							vol_time[m] = each.find_by_xpath('div/div/span/time').first.value
						if each.find_by_xpath('div/div/span/span'):
							vol_locality[m] = each.find_by_xpath('div/div/span/span').first.value
						if each.find_by_xpath('div/div/p'):
							vol_content[m] = each.find_by_xpath('div/div/p').first.value

						content = u"VOL_TITLE[%d]: %s\n" % (m, vol_title[m]) + u"VOL_ORG[%d]: %s\n" % (m, vol_org[m]) + u"VOL_TIME[%d]: %s\n" % (m, vol_time[m]) + u"VOL_LOCALITY[%d]: %s\n" % (m, vol_locality[m]) + u"VOL_CONTENT[%d]: %s\n" % (m, vol_content[m])
						f.write(content)
						m += 1
					except Exception, e:
						print "[Error]Volunteer Each: %s" % e
				else:
					break

		except Exception, e:
			print "[Error]Volunteer: %s" % e

		for i in range(0,5):
			temp = 75
			col_val[i*5 + temp] = vol_title[i]
			temp += 1
			col_val[i*5 + temp] = vol_org[i]
			temp += 1
			col_val[i*5 + temp] = vol_time[i]
			temp += 1
			col_val[i*5 + temp] = vol_locality[i]
			temp += 1
			col_val[i*5 + temp] = vol_content[i]

		#interest
		try:
			temp = browser.find_by_xpath('//*[@id="interests-view"]/ul/li[1]/a')
			if temp:
				interest_view = temp.first.value
				content = u"INTEREST_VIEW: %s\n" % interest_view
				f.write(content)
			
			col_val[100] = interest_view
		except Exception, e:
			print "[Error]Interest: %s" % e

		#languages
		try:
			languages = browser.find_by_id('languages-view');
			lang_li = [li for li in languages.find_by_xpath('ol/li')]
			n = 0
			for each in lang_li:
				if n <= 2:
					try:
						temp = each.find_by_xpath('h4/span[1]')
						if temp:
							lang_section[n] = temp.text
	
						n += 1
						content = u"LANG_SECTION[%d]: %s\n" % (n-1, lang_section[n-1])
						f.write(content)
					except Exception, e:
						print "[Error]Language each: %s" % e
				else:
					break

		except Exception, e:
			print "[Error]Language: %s" % e

		for i in range(0,3):
			temp = 101
			col_val[i + temp] = lang_section[i]

		#friends
		#try:
		#	friends_dir = browser.find_by_xpath('//*[@id="connections-view"]')
		#	friends_list = [li for li in friends_dir.find_by_xpath('div[2]/div/ul/li')]

			#friends
		#	i = 0
		#	for each in friends_list:
		#		if i <= 5:
		#			try:
		#				temp = each.find_by_xpath('strong/span/strong/a')
		#				if temp:
		#					friend_name[i] = temp.first.value
		#					friend_link[i] = temp.first['href']

						#store the friends_pic
		#				try:
		#					friend_picture_link = each.find_by_xpath("a[1]/span/strong/img")['src']
		#					temp = urllib2.urlopen(friend_picture_link)
		#					data = temp.read()
		#					urllib.urlretrieve(friend_picture_link, '%d-%d.png' % (sid, i))
		#					content = "FRIEND[%d]_PICTURE_LINK: " % i + friend_picture_link
		#					f.write(content)
		#				except Exception, e:
		#					print "[Error]Can't download %s %dth friend's photo: %s" %(sid, i, e)

		#				i += 1
		#				content = "FRIEND_NAME[%d]: %s\n" % (i-1, friend_name[i-1]) + "FRIEND_LINK[%d]: %s" % (i-1, friend_link[i-1])
		#				f.write(content) 

		#			except Exception, e:
		#				print "[Error]FriendList Each: %s" % e
		#		else:
		#			break
		#except Exception, e:
		#	print "[Error]Friends: %s" % e

		#ScreenShot
		try:
			if browser.status_code.is_success():
				browser.driver.save_screenshot('%d-ScreenShot.png' % sid)
		except socket.gaierror, e:
			print "[Error]%s" % e

		#try to download the profile picture
		try:
			profile_picture_link = browser.find_by_xpath("//*[@id='top-card']/div/div[1]/div[1]/a/img")['src']
			temp = urllib2.urlopen(profile_picture_link)
			time.sleep(0.5)
			data = temp.read()
			urllib.urlretrieve(profile_picture_link, '%d.png' % sid)
			
			content = u"PROFILE_PICTURE_LINK: " + profile_picture_link + u"\n"
			f.write(content)
		except Exception, e:
			print "[Error]Can't download %s's photo: %s" %(sid,e)

		#save the result
		for i in range(0,116):
			try:
				sh.write(col_count,i,col_val[i])
			except Exception, e:
				print "[Error]Save: %s" % e

		f.close
		book.save('linkedin.xls')
		col_count += 1
		
if __name__ == '__main__':
	#this is a people list of alumni that need to be fetched, the table format(.xls) follows below:
	#No	Name	Job	Place	Link
	#1	Joe Jiang	Engineer at Infineon Technologies	China	http://www.linkedin.com/profile/view?id=000000

	#you can also have a look at the 'result.xls' in the same path of this repo: /LinkedIn/result.xls

	read_singlepage('./result.xls')