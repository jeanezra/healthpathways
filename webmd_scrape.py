import requests
import bs4

website = 'http://exchanges.webmd.com/back-pain-exchange?login=true'

page = requests.get(website)

file_name = 'webmd_test.txt'

file_w = open(file_name, 'wb')
for chunk in page.iter_content(100000):
    file_w.write(chunk)
file_w.close()

link = 'http://forums.webmd.com/3/back-pain-exchange/forum/2555'

response = requests.get(link)
soup = bs4.BeautifulSoup(response.text)

title = str(soup.find('div', class_='first_item_title_format'))