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
    links = [a.attrs.get('href') for a in
             soup.select('.thread_fmt a[href^=http://forums.webmd.com/3/back-pain-exchange/forum/]')]
    print links
    print len(links)
    return links


# Find unique links
def scrape_unique_links(links):
    links_unq = unique_links(links)
    print len(links_unq)
    matching = [s for s in links_unq if "forum" in s]
    print len(matching)
    # download_iterator(matching, 'bp', len(links_unq))
    return matching


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


def title_data(soup):
    title_text = scrape_element(soup,'title','.first_item_title_fmt')
    df_title = DataFrame(pd.Series(len(title_text)))
    df_title.columns = ['title_length']
    return df_title


def messages_data(soup):
    messages = scrape_element(soup, 'messages', '.post_fmt')
    msg_lengths = []
    for k, v in messages.items():
        msg_lengths.append(len(v))
    df_msg_lgth = DataFrame(msg_lengths)
    df_msg_describe = DataFrame(df_msg_lgth.describe()).T
    cols = df_msg_describe.columns
    df_msg_describe.columns = ['msg_' + c for c in cols]
    return df_msg_describe


def create_date_diff(df_create, var, prefix):
    df_create_describe = DataFrame(df_create[[var]].describe()).T
    cols = df_create_describe.columns
    df_create_describe.columns = [prefix + c for c in cols]
    return df_create_describe


def posts_create_clean(dates):
    create_dates2 =[]
    for k, v in dates.items():
        create_dates2.append(v)
    print create_dates2
    df_create_dates2 = pd.DataFrame(create_dates2)
    df_create_dates2[1] = df_create_dates2[0].apply(lambda x: x.strip("document.write(DataDelta("))
    df_create_dates2[2] = df_create_dates2[1].apply(lambda x: x.replace("GMT-0400","").replace("(EDT)",""))
    df_create_dates2[3] = df_create_dates2[2].apply(lambda x: x.replace("GMT-0500","").replace("(EST)",""))
    df_create_dates2['dt'] = df_create_dates2[3].apply(lambda x: x.rstrip(');'))
    df_create_dates2['date'] = df_create_dates2['dt'].apply(lambda x: pd.to_datetime(x))
    df_create_dates2.sort_values('date',ascending=True,inplace=True)
    df_create_dates2.reset_index(inplace=True)
    return df_create_dates2


def posts_first_create(date):
    create_date = []
    create_date.append(date['dates0'])
    df_create_date = pd.DataFrame(create_date)
    df_create_date[1] = df_create_date[0].apply(lambda x: x.strip('\r\n\t'))
    df_create_date[2] = df_create_date[1].apply(lambda x: x.lstrip('Last Reply: '))
    df_create_date[3] = df_create_date[2].apply(lambda x: x.strip('\r\n\t '))
    df_create_date[4] = df_create_date[3].apply(lambda x: x.strip('\n\t'))
    df_create_date[5] = df_create_date[4].apply(lambda x: x.strip("document.write(DateDelta('"))
    df_create_date[6] = df_create_date[5].apply(lambda x: x.replace("GMT-0400","").replace("(EDT)",""))
    df_create_date[7] = df_create_date[6].apply(lambda x: x.replace("GMT-0500","").replace("(EST)",""))
    df_create_date['dt'] = df_create_date[7].apply(lambda x: x.rstrip(');'))
    df_create_date['date'] = df_create_date['dt'].apply(lambda x: pd.to_datetime(x))
    return df_create_date


def posts_create_data(soup):
    date = scrape_element(soup, 'dates', '.first_posted_fmt')
    dates = scrape_element(soup, 'dates', '.posted_fmt')
    if len(dates) == 0:
        df_create_dates3 = posts_first_create(date)
    else:
        df_create_date = posts_first_create(date)
        df_create_dates2 = posts_create_clean(dates)
        df_create_dates3 = pd.concat([df_create_date[['date']],df_create_dates2[['date']]],axis=0)
    df_create_dates3.reset_index(inplace=True)
    df_create_dates3 = df_create_dates3[['date']].sort_values('date',ascending=True)
    df_create_dates3.reset_index(inplace=True)
    df_create_dates3 = df_create_dates3[['date']].sort_values('date', ascending=True)
    date_size = len(df_create_dates3)
    df_next = df_create_dates3['date'].ix[1:date_size - 1].reset_index()
    df_next.columns = ['index', 'next_date']
    df_now_next = DataFrame(df_create_dates3['date']).join(DataFrame(df_next['next_date']))
    df_now_next['diff'] = (df_now_next['next_date'] - df_now_next['date']) / np.timedelta64(1, 'D')
    df_date = create_date_diff(df_now_next, 'date', 'create_').reset_index().drop('index', 1)
    df_diff = create_date_diff(df_now_next, 'diff', 'datediff_').reset_index().drop('index', 1).astype(float)
    dfs = pd.concat([df_date, df_diff], axis=1)
    return dfs


def combine_data(title, posts, create):
    all_data = pd.concat([title, posts, create], axis=1)
    print all_data.shape
    return all_data


def main():
    forum_link = 'http://exchanges.webmd.com/back-pain-exchange'
    web_links = scrape_links(forum_link)
    matching = scrape_unique_links(web_links)
i = 0
for m in matching:
    print i, '\n', datetime.now()
    response = requests.get(matching[i])
    print matching[i]
    soup = bs4.BeautifulSoup(response.text)
    df_title = title_data(soup)
    df_msg = messages_data(soup)
    df_date = posts_create_data(soup)
    all_data = combine_data(df_title, df_msg, df_date)
    if i == 0:
        all_data.to_csv('back_pain.csv', delimiter=',', header=True, index=True, mode='w')
    else:
        all_data.to_csv('back_pain.csv', delimiter=',', header=False, index=True, mode='a')
    i += 1



# MAIN CODE
if __name__="__main__":
    main()

# # More than one page?
# pages = soup.select('.pages')
# print len(pages)