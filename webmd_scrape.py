import requests
import bs4

website = 'http://exchanges.webmd.com/back-pain-exchange?login=true'



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


# Find unique links
def scrape_unique_links(links):
    links_unq = unique_links(links)
    print len(links_unq)
    matching = [s for s in links_unq if "#latest" in s]
    print len(matching)
    download_iterator(matching, 'lbp', len(links_unq))
    return matching


link = 'http://forums.webmd.com/3/back-pain-exchange/forum/2555'
link = 'http://ehealthforum.com/health/chronic-pain-on-walking-sitting-lying-down-or-twisting-t484348.html'

response = requests.get(link)
soup = bs4.BeautifulSoup(response.text)

# msg = soup.select('.vt_post_body')

title = soup.select('.first_item_title_fmt')
print len(title)
print title

msg = soup.select('.post_fmt')
print len(msg)

date = soup.select('.first_posted_fmt')
print len(date)

dates = soup.select('.posted_fmt')
print len(dates)

expert = soup.select('.expert_badge_fmt')
print len(expert)

# More than one page?
pages = soup.select('.pages')
print len(pages)