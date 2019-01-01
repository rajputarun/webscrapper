# div class_=poster --> a['href'] --> div[1] class_=pswp__zoom-wrap --> img[1]['src']

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

class Film():
	"""docstring for Film"""
	def __init__(self):		
		self.rank = ""
		self.title = ""		
		self.year = ""
		self.link = ""


def get_film_list():

	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

	url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'

	driver.get(url)

	# print driver.page_source

	soup = BeautifulSoup(driver.page_source,'lxml')

	table = soup.find('table', class_ = 'chart')

	film_list = []

	for td in table.find_all('td', class_ = 'titleColumn'):
		
		full_title = td.text.strip().replace('\n','').replace('      ','')
		print full_title

		rank = full_title.split('.')[0]
		print rank

		title = full_title.split('.')[1].split('(')[0]
		print title

		year = full_title.split('(')[1][:-1]
		print year

		a = td.find('a')
		print a['href']

		print '\n'

		new_film = Film()
		new_film.rank = rank
		new_film.title = title
		new_film.year = year
		new_film.link = a['href']

		film_list.append(new_film)

	driver.quit()

	return film_list


def download_all_posters(film_list):

	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	
	for film in film_list:


		# url = 'http://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=0PS12P50E86XYMR1RVR3&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1'

		url = 'http://www.imdb.com/' + film.link

		driver.get(url)

		soup = BeautifulSoup(driver.page_source,'lxml')

		div = soup.find('div', class_ = 'poster')

		a = div.find('a')

		# print 'http://www.imdb.com' + a['href']

		url = 'http://www.imdb.com' + a['href']

		driver.get(url)

		soup = BeautifulSoup(driver.page_source, 'lxml')

		all_div = soup.find_all('div', class_ = 'pswp__zoom-wrap')

		all_img = all_div[1].find_all('img')

		print all_img[1]['src']

		f = open('{0}.jpg'.format(film.title.encode('utf8').replace(':','')), 'wb')
		f.write(requests.get(all_img[1]['src']).content)
		f.close()

	driver.quit()


download_all_posters( get_film_list() )