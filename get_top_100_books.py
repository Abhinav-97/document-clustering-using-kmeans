import requests
import lxml.html
from bs4 import BeautifulSoup
import pickle

def get_top_books(page):

	soup = BeautifulSoup(page.text, 'html.parser')
	# print(data)
	content = soup.find('div',{'class':'content'})
	main_content_container = content.find('div', {'class': 'mainContentContainer'})
	main_content = main_content_container.find('div', {'class':'mainContent'})
	# print(main_content.encode('utf-8'))
	main_content_float = main_content.find('div', {'class':'mainContentFloat'})
	left_container = main_content_float.find('div', {'class':'leftContainer'})
	# print(left_container.encode('utf-8'))
	all_votes = main_content_float.find('div', {'class':'all_votes'})
	table_elements = left_container.find('table') 
	# print(table_elements.encode('utf-8'))
	# left_table_rows = leftContainer.find('table').find('tbody')
	table_rows = table_elements.find_all('tr')
	# print(table_rows.encode('utf-8'))
	books = []
	for rows in table_rows:
		td = rows.find('td',{'valign':'top', 'width':'100%'})
		book_name = td.find('span').text
		print(book_name)
		books.append(book_name)
	with open('book_names.txt',mode='wt',encoding='utf-8') as fp:
		fp.write('\n'.join(str(book) for book in books)) 

s = requests.session()

login = s.get('https://www.goodreads.com/user/sign_in')
login_html = lxml.html.fromstring(login.text)
hidden_input = login_html.xpath(r'//div[@class="wrapper"]//div[@class="content distractionless"]//div[@class="mainContentContainer"]//div[@class="mainContent"]//div[@class="contentBox clearfix"]//div[@class="column_right"]//div[@id="emailForm"]//form//input[@type="hidden"]')
# print(hidden_input)
form = { x.attrib["name"]: x.attrib["value"] for x in hidden_input }

# for key, value in form.items():
# 	print(key.encode('utf-8'))
# 	print(value.encode('utf-8'))

form['user[email]']='abhinavdutt19@gmail.com'
form['user[password']='abhi97dutt'

response = s.post('https://www.goodreads.com/user/sign_in', data=form)

url = 'https://www.goodreads.com/list/show/2681.Time_Magazine_s_All_Time_100_Novels'
url_client = s.get(url)
get_top_books(url_client)