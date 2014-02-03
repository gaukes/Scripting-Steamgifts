from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import selenium, time

def success_but_check(_):
	try:
		return browser.find_element_by_xpath('//*[@id="success_continue_btn"]/h3')
	except selenium.common.exceptions.NoSuchElementException:
		return False

def gmail_opener():
	mail_browser = webdriver.Chrome()
	mail_browser.get("https://accounts.google.com/ServiceLogin?service=mail&continue=https://mail.google.com/mail/&hl=en") # you may want to change this section if you use a different email client
	mail_browser.find_element_by_id("Email").send_keys("***** ENTER EMAIL HERE *****")
	mail_browser.find_element_by_id("Passwd").send_keys("***** ENTER PASSWORD HERE *****")
	mail_browser.find_element_by_id("signIn").click()
	try:
		mail_browser.find_element_by_id("no-button").click()
	except selenium.common.exceptions.NoSuchElementException:
		pass
	WebDriverWait(mail_browser, 10).until(EC.title_contains('Inbox'))
	mail_browser.find_element_by_name("Steam Support").click()
	WebDriverWait(mail_browser, 10).until(EC.title_contains('Steam'))
	try:
		mail_browser.find_element_by_link_text("Verify Login Information")
	except selenium.common.exceptions.NoSuchElementException:
		mail_browser.find_element_by_class_name('ajT').click()
	code_list = mail_browser.find_elements_by_tag_name('h2')
	code_text = ''.join([item.text for item in mail_browser.find_elements_by_tag_name('h2')])
	if 'Chat' in code_text:
		code_text = code_text.replace('Chat', '')
	mail_browser.quit()
	return code_text

def login_rep_helper():
	code = gmail_opener()
	browser.find_element_by_id('authcode').clear()
	browser.find_element_by_id('authcode').send_keys(code)
	browser.find_element_by_id('friendlyname').send_keys('mycomp')
	time.sleep(1)
	try:
		browser.find_element_by_xpath('//*[@id="auth_buttonset_entercode"]/a[1]').click()
	except selenium.common.exceptions.ElementNotVisibleException:
		browser.find_element_by_xpath('//*[@id="auth_buttonset_incorrectcode"]/a[1]').click()


def steam_login():
	browser.find_element_by_id("steamAccountName").send_keys("***** ENTER STEAM ACCOUNT NAME HERE *****")
	browser.find_element_by_id("steamPassword").send_keys("***** ENTER PASSWORD HERE *****")
	browser.find_element_by_id("login_btn_signin").click()
	login_rep_helper()
	try:
		if ('Whoops!' in browser.find_element_by_xpath('//*[@id="auth_message_incorrectcode"]/h1').text):
			login_rep_helper()
	except selenium.common.exceptions.NoSuchElementException:
		pass
	WebDriverWait(browser, 15).until(EC.visibility_of(browser.find_element_by_xpath('//*[@id="success_continue_btn"]/h3')))
	browser.find_element_by_xpath('//*[@id="success_continue_btn"]').click()
	WebDriverWait(browser, 30).until(EC.title_contains('Steam Gifts'))

def point_updater():
	try:
		points = browser.find_element_by_xpath('//*[@id="navigation"]/ol/li[3]/a').text[9:]
		points = points[:points.index('P')]
		return int(points)
	except selenium.common.exceptions.NoSuchElementException:
		points = 300
		print('point_updater has failed. Please tweak program.')
		pass

def post_search(link):
	browser.get(link)
	post_dict = {}
	for post in browser.find_elements_by_class_name('post'):
		try:
			temp = post.find_element_by_class_name('title').find_element_by_tag_name('a')
			if 'http' in temp.get_attribute('href'):
				print(temp.get_attribute('href'))
				post_dict[temp.text] = temp.get_attribute('href')
		except selenium.common.exceptions.NoSuchElementException:
			pass
	return post_dict

def magic_clicker(post_dict):
	for post in post_dict:
		if post not in black_list:
			browser.get(post_dict[post])
			entry_button = browser.find_element_by_xpath('//*[@id="form_enter_giveaway"]/a')
			if 'Remove Entry' not in entry_button.text:
				entry_button.click()

browser = webdriver.Chrome()
browser.get("http://steamgifts.com")
browser.find_element_by_class_name("login").click()

steam_login()

page_num = 1
link_to_go = 'http://www.steamgifts.com/open/page/{0}'.format(page_num)
points = point_updater()
black_list = [] # add any games you dont want into the black list. Make sure you copy the name the same way as the program reads it

while points > 10:
	magic_clicker(post_search(link_to_go))
	page_num += 1
	points = point_updater()

print('Done')