import requests

# Download file
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


download_website('http://www.spine-health.com/forum/discussion/90643/pain/lower-back-pain/l5s1-when-consider-surgery','link1.txt')

websites = ['http://www.spine-health.com/forum/discussion/90643/pain/lower-back-pain/l5s1-when-consider-surgery',
            'http://www.spine-health.com/forum/discussion/90590/pain/lower-back-pain/normal-scans-still-pretty-severe-pain',
            'http://www.spine-health.com/forum/discussion/90632/pain/lower-back-pain/pain-extending-flexing',
            'http://www.spine-health.com/forum/discussion/90640/pain/lower-back-pain/synovial-cyst-l4-l5-bulge-pain-anyone-want-chat-future-coping',
            'http://www.spine-health.com/forum/discussion/90626/pain/lower-back-pain/degenerative-osteoarthritis-after-car-crash'
            ]

num = range(1,6)
file_names = ['link' + str(c) + '.txt' for c in num]
print file_names

for i,j in zip(websites,file_names):
    download_website(i,j)
    print j