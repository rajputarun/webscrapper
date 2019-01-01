# div class_=poster --> a['href'] --> div[1] class_=pswp__zoom-wrap --> img[1]['src']

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

url = 'http://www.imdb.com/title/tt0111161/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=0PS12P50E86XYMR1RVR3&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_1'

driver = webdriver.PhantomJS(executable_path = r'C:\phantomjs-2.1.1-windows\bin\phantomjs.exe')

driver.get(url)

soup = BeautifulSoup(driver.page_source,'lxml')

div = soup.find('div', class_ = 'poster')

a = div.find('a')

print 'http://www.imdb.com' + a['href']

url = 'http://www.imdb.com' + a['href']

driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

all_div = soup.find_all('div', class_ = 'pswp__zoom-wrap')

all_img = all_div[1].find_all('img')

print all_img[1]['src']

f = open('first_image.jpg', 'wb')
f.write(requests.get(all_img[1]['src']).content)
f.close()

driver.quit()




