
# coding: utf-8

# In[69]:


from bs4 import BeautifulSoup
import requests
import re
import os
import urllib


# In[3]:


url='https://cblog.site/index.html'
base = 'https://cblog.site/'


# In[4]:


res = requests.get(url)


# In[10]:


soup = BeautifulSoup(res.content, 'html5lib')


# In[61]:


category_tag = soup.select('section[class=category] ul li a')


# In[64]:


category = []
for item in category_tag:
    category.append((re.search('\d+', item.attrs['href']).group(), item.text, item.attrs['href']))


# In[65]:


category


# In[70]:





# In[81]:


posts = []
posts_tag = soup.select('section[class=content] article header div h1 a')
for item in posts_tag:
    id = re.search('\d+', item.attrs['href']).group()
    title = item.text
    link = item.attrs['href']
    tmp = BeautifulSoup(requests.get(urllib.parse.urljoin(base, link)).content, 'html5lib')
    cont = tmp.select('section[class=content] article div[class=body]')[0].text
    about = tmp.select('section[class=content] article header div div')[0].text
    posts.append((id, title, cont, about))


# In[82]:


posts


# In[84]:


category_post = {}
for (id, cate, link) in category:
    category_post[id] = []
    nl = urllib.parse.urljoin(base, link)
    tmp = BeautifulSoup(requests.get(nl).content, 'html5lib')
    tag = tmp.select('section[class=content] article header div h1 a')
    for k in tag:
        pid = re.search('\d+', k.attrs['href']).group()
        category_post[id].append(pid)


# In[86]:


category_post, category, posts


# In[87]:


import sqlite3


# In[120]:


sqlite = sqlite3.connect('/home/jue/workspace/cblog.site/instance/cblog.sqlite')


# In[116]:


category = sorted(category, key = lambda d:int(d[0]))
for item in category:
    sqlite.execute('insert into category(id, value, user_id) values(?, ?, ?)' ,(int(item[0]), item[1], 1))
    sqlite.commit()


# In[121]:


posts = sorted(posts, key = lambda d:int(d[0]))
for item in posts:
    sqlite.execute('insert into post(id, author_id, created, title, body) values(?, ?, ?, ?, ?)', (int(item[0]), 1,  re.search('\d+-\d+-\d+', item[3]).group(), item[1], item[2]))
sqlite.commit()


# In[123]:


for key in category_post:
    lst = category_post[key]
    lst.sort()
    for k in lst:
        sqlite.execute('insert into category_post(category_id, post_id) values(?, ?)', (key, k))
    sqlite.commit()


# In[124]:


sqlite.close()

