import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_financial_statements(code):
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=0&freq_typ=Y" % (code)
    html = requests.get(url).text

    html = html.replace('<th class="bg r01c02 endLine line-bottom"colspan="8">연간</th>', "")
    html = html.replace("<span class='span-sub'>(IFRS연결)</span>", "")
    html = html.replace("<span class='span-sub'>(IFRS별도)</span>", "")
    html = html.replace("<span class='span-sub'>(GAAP개별)</span>", "")
    html = html.replace('\t', '')
    html = html.replace('\n', '')
    html = html.replace('\r', '')

    for year in range(2009, 2018):
        for month in range(6, 13):
            month = "/%02d" % month
            html = html.replace(str(year) + month, str(year))

        for month in range(1, 6):
            month = "/%02d" % month
            html = html.replace(str(year+1) + month, str(year))

        html = html.replace(str(year) + '(E)', str(year))

    df_list = pd.read_html(html, index_col='주요재무정보')
    df = df_list[0]
    return df

def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2016"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    tr_data = soup.find_all('tr', id='tr_288401_1')
    td_data = tr_data[0].find_all('td')

    treasury_3year = {}
    start_year = 1998

    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1

    print(treasury_3year)
    return treasury_3year

if __name__ == "__main__":
    #df = get_financial_statements('035720')
    #print(df)
    get_3year_treasury()


