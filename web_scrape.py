from lxml import html
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


def naming_links(prefix):
    num = range(1,6)
    file_names = [prefix + '_' + str(c) + '.txt' for c in num]
    print file_names
    return file_names


def site_iterator(websites,file_names):
    for i,j in zip(websites,file_names):
        download_website(i,j)
        print 'Created ', j


def main(websites):
    file_names = naming_links('preg')
    site_iterator(websites,file_names)
    print 'Downloaded websites'


response = requests.get('http://www.spine-health.com/forum/categories/lower-back-pain')
soup = bs4.BeautifulSoup(response.text)
print soup
links = soup.select('#Body a[href^=http://www.spine-health.com/forum/discussion]')
print links
print len(links)

response = requests.get('http://pyvideo.org/category/50/pycon-us-2014')
links = soup.select('div.video-summary-data a[href^=/video]')

# MAIN CODE
# if __name__="__main__":
#     main(websites)
# Back pain
websites = ['http://www.spine-health.com/forum/discussion/90643/pain/lower-back-pain/l5s1-when-consider-surgery',
            'http://www.spine-health.com/forum/discussion/90590/pain/lower-back-pain/normal-scans-still-pretty-severe-pain',
            'http://www.spine-health.com/forum/discussion/90632/pain/lower-back-pain/pain-extending-flexing',
            'http://www.spine-health.com/forum/discussion/90640/pain/lower-back-pain/synovial-cyst-l4-l5-bulge-pain-anyone-want-chat-future-coping',
            'http://www.spine-health.com/forum/discussion/90626/pain/lower-back-pain/degenerative-osteoarthritis-after-car-crash'
            ]

# Pregnancy - complications
# Source: http://www.whattoexpect.com/forums/complications.html
websites = ['http://www.whattoexpect.com/forums/complications/topic/abnormal-labs.html',
            'http://www.whattoexpect.com/forums/complications/topic/13-week-u-s-left-side-of-the-heart-is-smaller-any-similar-experiences.html',
            'http://www.whattoexpect.com/forums/complications/topic/baby-is-here-3285.html',
            'http://www.whattoexpect.com/forums/complications/topic/cerclage-and-still-bleeding-help.html',
            'http://www.whattoexpect.com/forums/complications/topic/toxoplasmosis-question-48.html']