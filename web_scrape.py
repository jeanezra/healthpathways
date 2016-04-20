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


def naming_links(prefix,num_files):
    num = range(1,num_files+1)
    file_names = [prefix + '_' + str(c) + '.txt' for c in num]
    print file_names
    return file_names


def site_iterator(websites,file_names):
    for i,j in zip(websites,file_names):
        download_website(i,j)
        print 'Created ', j


def main(websites,prefix,num_files):
    file_names = naming_links(prefix,num_files)
    site_iterator(websites,file_names)
    print 'Downloaded websites'


response = requests.get('http://www.spine-health.com/forum/categories/lower-back-pain')
soup = bs4.BeautifulSoup(response.text)
# links = soup.select('#Body a[href^=http://www.spine-health.com/forum/discussion]')
links = [a.attrs.get('href') for a in soup.select('#Body a[href^=http://www.spine-health.com/forum/discussion]')]
print links
print len(links)

def unique_links(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output

links_unq = unique_links(links)
print len(links_unq)

matching = [s for s in links_unq if "#latest" in s]
len(matching)
main(matching,'lbp',30)

def get_patient_data(patient_page_url):
    response = requests.get('http://www.spine-health.com/forum/discussion/77790/pain/lower-back-pain/lumbar-spine-locked#latest')
    soup = bs4.BeautifulSoup(response.text)
    patient_data = {}
    patient_data['message'] = soup.select('.Message').get_text()
    patient_data['speakers'] = [a.get_text() for a in soup.select('div#sidebar a[href^=/speaker]')]
    patient_data['youtube_url'] = soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text()

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