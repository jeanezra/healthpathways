import requests
import bs4



# FUNCTIONS
def download_website(website,file_name):
    page = requests.get(website)
    try:
        page.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    file = open(file_name,'wb')
    for chunk in page.iter_content(100000):
        file.write(chunk)
    file.close()


def naming_links(prefix,num_files):
    num = range(1,num_files+1)
    file_names = [prefix + '_' + str(c) + '.txt' for c in num]
    print file_names
    return file_names


def site_iterator(websites,file_names):
    for i,j in zip(websites,file_names):
        download_website(i,j)
        print 'Created ', j


def unique_links(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output


def main(websites,prefix,num_files):
    file_names = naming_links(prefix,num_files)
    site_iterator(websites,file_names)
    print 'Downloaded websites'


def scrape_element(prefix,element):
    messages = soup.select(element)
    length = len(messages)
    print length
    n = range(0,length)
    print n
    dict = {}
    for i in n:
        dict[prefix+str(i)] = soup.select(element)[i].get_text()
    return dict


# Scraping weblinks
response = requests.get('http://www.spine-health.com/forum/categories/lower-back-pain')
soup = bs4.BeautifulSoup(response.text)
links = [a.attrs.get('href') for a in soup.select('#Body a[href^=http://www.spine-health.com/forum/discussion]')]
print links
print len(links)

# Find unique links
links_unq = unique_links(links)
print len(links_unq)
matching = [s for s in links_unq if "#latest" in s]
len(matching)
main(matching,'lbp',len(links_unq))

# Scraping pages
response = requests.get('http://www.spine-health.com/forum/discussion/77790/pain/lower-back-pain/lumbar-spine-locked#latest')
soup = bs4.BeautifulSoup(response.text)
# Metadata
forum = scrape_element('forum','.MItem.Category')
title = soup.find('div',class_='PageTitle').h1
# Data
messages = scrape_element('messages','.Message')
posts_cnt = scrape_element('posts_cnt','.MItem.PostCount')
created = scrape_element('created','.MItem.DateCreated')
updated = scrape_element('updated','.DateUpdated')
author = scrape_element('author','.Author')

# MAIN CODE
# if __name__="__main__":
#     main(websites)