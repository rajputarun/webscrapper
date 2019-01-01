from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

class Film(object):
	"""docstring for film"""
	def __init__(self):
		self.title = ""
		self.rank = ""
		self.year_of_production = ""
		self.link = ""
		
def create_phantom_driver():
	driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
	return driver

def get_popular_film_list(url):

	driver = create_phantom_driver()

	# url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'

	# download html
	driver.get(url)

	# print driver.page_source

	# create soup
	soup = BeautifulSoup(driver.page_source,'lxml')

	# soup = BeautifulSoup(open('imdb.html'),'lxml')

	# search
	table = soup.find('table',class_='chart')

	film_list =[]

	for td in table.find_all('td',class_='titleColumn'):

		a = td.find('a')
		# print a['href']

		new_film = Film()		

		full_des = td.text.strip().replace('\n','')

		# print full_des

		title = full_des.split('(')[0]
		# print title
		year  = full_des.split('(')[1][:4]
		# print year
		start_rank  = full_des.find(')')
		end_rank = full_des.find('(',start_rank,len(full_des))
		rank = full_des[start_rank+1:end_rank]
		# print rank
		
		new_film.rank = rank
		new_film.title = title		
		new_film.year_of_production = year
		new_film.link = a['href'].strip()

		film_list.append(new_film)


	driver.quit()

	for film in film_list:
		print film.title
		print film.rank
		print film.year_of_production
		print film.link
		print "\n"

	return film_list



# when ever we have the film list
def poster_scrap(film_list):

	driver = create_phantom_driver()

	for film in film_list:		

		url = 'http://www.imdb.com' + film.link

		print film.title
		driver.get(url)
		soup = BeautifulSoup(driver.page_source, 'lxml')

		div = soup.find('div', class_='poster')

		# find the link lead to poster image
		a = div.find('a')

		# link to download poster image
		poster_url = 'http://www.imdb.com' + a['href']
		print poster_url

		driver.get(poster_url)
		soup = BeautifulSoup(driver.page_source, 'lxml')

		# print soup.prettify()
		
		divs = soup.find_all('div',class_='pswp__zoom-wrap')

		try:
			imgs = divs[1].find_all('img')
			download_link = imgs[1]['src']
			print download_link
		except Exception, e:			
			imgs = divs[0].find_all('img')
			download_link = imgs[1]['src']
			print download_link

		

		f = open('{0}.jpg'.format(film.title.encode('utf8').replace(':','')),'wb')
		f.write(requests.get(download_link).content)
		# time.sleep(2)
		f.close()

	driver.quit()


# url for current popular and hot film
url = 'http://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm_7'
# get_popular_film_list(url)
poster_scrap(get_popular_film_list(url))
