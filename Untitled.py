#!/usr/bin/env python
# coding: utf-8

# In[15]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[46]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[47]:


tesla=yf.Ticker('TSLA')


# In[48]:


tesla_data=tesla.history(period="max")


# In[49]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[50]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[81]:


soup = BeautifulSoup(html_data, "html5lib")



# In[94]:


tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
tables = soup.find_all("table")
for table in tables:
    rows = table.find_all("tr")
    # Check if the table has rows and extract data accordingly
    if len(rows) > 0:
        for row in rows:
            cols = row.find_all("td")
            date = col[0].text
            revenue = col[1].text
            tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)

tesla_revenue.head()


# In[95]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")


# In[96]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[97]:


tesla_revenue.tail()


# In[98]:


gme = yf.Ticker("GME")


# In[99]:


gme_data = gme.history(period="max")


# In[100]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[111]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text


# In[119]:


beautiful_soup=BeautifulSoup(html_data,"html.parser")


# In[120]:


tables=beautiful_soup.find_all("table")
for index,table in enumerate(tables):
    if(str(table)=="GameStop Quarterly Revenue"):
        table_index=index

gme_revenue=pd.DataFrame(columns=["Date","Revenue"])

for row in tables[table_index].tbody.find_all("tr"):
    col=row.find_all("td")
    if(col!=[]):
        date=col[0].text
        revenue=col[1].text.replace("$","").replace(",","")
        gme_revenue=gme_revenue.append({"Date":date,"Revenue":revenue},ignore_index=True)
gme_revenue.head()


# In[ ]:





# In[118]:


gme_revenue.tail(5)


# In[121]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[122]:


make_graph(gme_data,gme_revenue,'GameStop')


# In[ ]:




