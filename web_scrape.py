import requests

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



# link 1
# 4/12; 2:55pm
# physical therapy for several months - no relief.
# Symptoms getting worse.
# Bulge on L4-L5
# Foot feels broken and lower back and rear end constanting burning
# Two small children, one is an infant so wanting to avoid surgery
# Surgery may be only hope
# Neurologist doing some shots but I don't see him until Monday

# link 2
# 4/9; 2:03pm
# 6 months ago, pretty severe lumbar pain, apparent when bending down - so thought muscular
# February, saw orthopedist, x-ray, told slight scoliosis, but most likely won't cause it
# Cause of bending over, I felt stabbing pain, so got a second opinion at neurologist, ordered MRI with and without contract
# MRI showed everything normal, but still in severe pain
# Diagnosed with sciatica due to shooting, sharop, pains down my leg - told to take aleve and maybe PT
# Lost of what to do, as nothing helps, nor any diagnosis
# Orthopedist visit gave exercises that couldn't be completed due to excrutiating pain
# Morning, pains seems more severe
# No injuries over last 6 months to have caused such a thing
# Believe is muscular but wouldn't cause pain and would have healed by now
# Heard MRIs aren't good for diagnosing problems with lumbar spine
# Feel pain is most severe if bending slightly backwards and bending over

# Diagnosis - Sciatica, Bulging disks L4-L5
# Specialists - Neurologist for pain shots; orthopedist for exercises
# Symptoms - Foot broken, lower back/rear end constant burning; worse in the morning
# Physical Therapy - didn't work
# Time Duration - 6 months ago thought it was muscle problem
# Psychosocial Aspects - have 2 small children and want to avoid surgery; heard MRIs are no use