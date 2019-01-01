# How to working with paging
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

		
def create_phantom_driver():
	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	return driver


def get_download_link_one_page(url):

	link_list_one_page = []

	driver = create_phantom_driver()

	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'lxml')

	div = soup.find('div', class_ = 'media_index_thumb_list')

	for a in div.find_all('a'):
		# print a['href']
		link_list_one_page.append(a['href'])

	driver.quit()

	return link_list_one_page

# when ever we have the film list
def get_download_link_all_pages():

	max_page = 1
	link_list_all_page = []

	for page_number in range(1, max_page + 1):		
		page_url = 'http://www.imdb.com/gallery/rg1528338944?page={0}&ref_=rgmi_mi_sm'.format(page_number)
		link_list_all_page.extend(get_download_link_one_page(page_url))

	for link in link_list_all_page:
		print link

	return link_list_all_page


def download_all_poster(link_list_all_page):

	driver = create_phantom_driver()	

	for link in link_list_all_page:

		driver.get('http://www.imdb.com'+link)

		soup = BeautifulSoup(driver.page_source,'lxml')

		
		# get jpeg link
		divs = soup.find_all('div', class_= 'pswp__zoom-wrap')
		imgs = divs[1].find_all('img')
		jpg_link = imgs[1]['src']		
		print imgs[1]['src']

		# get image title
		div = soup.find('div', class_ = 'mediaviewer__footer')
		p = div.find('p')
		jpg_title = p.text
		print p.text

		# lets download the image
		f = open('{0}.jpg'.format(jpg_title.encode('utf8').replace(':','')),'wb')
		f.write(requests.get(jpg_link).content)
		f.close()

	driver.quit()


download_all_poster(get_download_link_all_pages())

