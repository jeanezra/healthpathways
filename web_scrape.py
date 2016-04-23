import requests
import bs4
import pandas as pd


# FUNCTIONS
def download_website(website, file_name):
    page = requests.get(website)
    try:
        page.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    file_w = open(file_name, 'wb')
    for chunk in page.iter_content(100000):
        file_w.write(chunk)
    file_w.close()


def naming_links(prefix, num_files):
    num = range(1, num_files + 1)
    file_names = [prefix + '_' + str(c) + '.txt' for c in num]
    print file_names
    return file_names


def site_iterator(websites, file_names):
    for i, j in zip(websites, file_names):
        download_website(i, j)
        print 'Created ', j


def unique_links(link):
    output = []
    for x in link:
        if x not in output:
            output.append(x)
    return output


def download_iterator(websites, prefix, num_files):
    file_names = naming_links(prefix, num_files)
    site_iterator(websites, file_names)
    print 'Downloaded websites'


# Scraping web links
def scrape_links(link):
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text)
    links = [a.attrs.get('href') for a in soup.select('#Body a[href^=http://www.spine-health.com/forum/discussion]')]
    print links
    print len(links)
    return links

forum_link = 'http://www.spine-health.com/forum/categories/lower-back-pain'

web_links = scrape_links(forum_link)


# Find unique links
def scrape_unique_links(links):
    links_unq = unique_links(links)
    print len(links_unq)
    matching = [s for s in links_unq if "#latest" in s]
    print len(matching)
    download_iterator(matching, 'lbp', len(links_unq))


scrape_unique_links(web_links)


# Scraping page
def scrape_element(prefix, element):
    msgs = soup.select(element)
    length = len(msgs)
    print length
    n = range(0, length)
    print n
    element_dict = {}
    for i in n:
        element_dict[prefix + str(i)] = soup.select(element)[i].get_text()
    return element_dict



response = requests.get('http://www.spine-health.com/forum/discussion/77790/pain/lower-back-pain/lumbar-spine-locked#latest')
soup = bs4.BeautifulSoup(response.text)
# Metadata
# forum = scrape_element('forum', '.MItem.Category')
title = soup.find('div', class_='PageTitle').h1
# Data

# Distributions
# Length per post
messages = scrape_element('messages', '.Message')
msg_lengths = []
for k,v in messages.items():
    msg_lengths.append(len(v))

df_msg_lgth = pd.DataFrame(msg_lengths)
df_msg_lgth.describe()

# Author post history
posts_cnt = scrape_element('posts_cnt', '.MItem.PostCount')
posts_cnts = []
for k,v in posts_cnt.items():
    posts_cnts.append(v)

print posts_cnts
df_posts_cnts = pd.DataFrame(posts_cnts)
df_strip = df_posts_cnts[0].apply(lambda x: int(x.strip('Posts: ').replace(',','')))
df_strip.describe()



created = scrape_element('created', '.MItem.DateCreated')
updated = scrape_element('updated', '.DateUpdated')
author = scrape_element('author', '.Author')

# MAIN CODE
# if __name__="__main__":
#     main(websites)
