import requests
import bs4
import pandas as pd
from pandas import DataFrame
import numpy as np
from datetime import datetime


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
    # download_iterator(matching, 'lbp', len(links_unq))
    return matching


# Scraping page
def scrape_element(soup, prefix, element):
    msgs = soup.select(element)
    length = len(msgs)
    print length
    n = range(0, length)
    print n
    element_dict = {}
    for i in n:
        element_dict[prefix + str(i)] = soup.select(element)[i].get_text()
    return element_dict


# Metadata
# forum = scrape_element('forum', '.MItem.Category')
def title_data(soup):
    title = str(soup.find('div', class_='PageTitle').h1)
    title_text = title.replace('<h1>', '').replace('</h1>', '')
    df_title1 = DataFrame(pd.Series(title_text))
    df_title2 = DataFrame(pd.Series(len(title_text)))
    df_title = pd.concat([df_title1,df_title2],axis=1)
    df_title.columns = ['title','title_length']
    return df_title


# Data
# Distributions
# Length per post
def messages_data(soup):
    messages = scrape_element(soup, 'messages', '.Message')
    msg_lengths = []
    for k, v in messages.items():
        msg_lengths.append(len(v))
    df_msg_lgth = DataFrame(msg_lengths)
    df_msg_describe = DataFrame(df_msg_lgth.describe()).T
    cols = df_msg_describe.columns
    df_msg_describe.columns = ['msg_' + c for c in cols]
    return df_msg_describe


# Author post history
def posts_cnt_data(soup):
    posts_cnt = scrape_element(soup, 'posts_cnt', '.MItem.PostCount')
    posts_cnts = []
    for k, v in posts_cnt.items():
        posts_cnts.append(v)
    print posts_cnts
    df_posts_cnts = pd.DataFrame(posts_cnts)
    df_strip = df_posts_cnts[0].apply(lambda x: int(x.strip('Posts: ').replace(',', '')))
    df_strip_describe = DataFrame(df_strip.describe()).T
    cols = df_strip_describe.columns
    df_strip_describe.columns = ['postshistory_' + c for c in cols]
    return df_strip_describe


# Post created dates
def create_date_diff(df_create, var, prefix):
    df_create_describe = DataFrame(df_create[[var]].describe()).T
    cols = df_create_describe.columns
    df_create_describe.columns = [prefix + c for c in cols]
    return df_create_describe


def posts_create_data(soup):
    created = scrape_element(soup, 'created', '.MItem.DateCreated')
    create_dates = []
    for k, v in created.items():
        create_dates.append(v)
    print create_dates
    df_create_dates = pd.DataFrame(create_dates)
    df_create_dates[1] = df_create_dates[0].apply(lambda x: x.replace('\n', '').replace('Today',datetime.today().strftime("%m/%d/%Y")))
    df_create_dates['date'] = df_create_dates[1].apply(lambda x: pd.to_datetime(x))
    date_size = len(df_create_dates)
    df_next = df_create_dates['date'].ix[1:date_size - 1].reset_index()
    df_next.columns = ['index', 'next_date']
    df_now_next = DataFrame(df_create_dates['date']).join(DataFrame(df_next['next_date']))
    df_now_next['diff'] = (df_now_next['next_date'] - df_now_next['date']) / np.timedelta64(1, 'D')
    df_date = create_date_diff(df_now_next, 'date', 'create_').reset_index().drop('index', 1)
    df_diff = create_date_diff(df_now_next, 'diff', 'datediff_').reset_index().drop('index', 1).astype(float)
    dfs = pd.concat([df_date, df_diff], axis=1)
    return dfs


def combine_data(title, author, posts, create):
    all_data = pd.concat([title, author, posts, create], axis=1)
    print all_data.shape
    return all_data


# updated = scrape_element('updated', '.DateUpdated')
# author = scrape_element('author', '.Author')
def main():
    forum_link = 'http://www.spine-health.com/forum/categories/lower-back-pain'
    web_links = scrape_links(forum_link)
    matching = scrape_unique_links(web_links)
i = 1
for m in matching:
    print m, '\n', i, '\n', datetime.now()
    response = requests.get(m)
    soup = bs4.BeautifulSoup(response.text)
    df_title = title_data(soup)
    df_msg = messages_data(soup)
    df_posts = posts_cnt_data(soup)
    df_date = posts_create_data(soup)
    all_data = combine_data(df_title, df_msg, df_posts, df_date)
    if i == 1:
        all_data.to_csv('lower_back_pain.csv', delimiter=',', header=True, index=True, mode='w')
    else:
        all_data.to_csv('lower_back_pain.csv', delimiter=',', header=False, index=True, mode='a')
    i += 1





# MAIN CODE
if __name__=="__main__":
    main()