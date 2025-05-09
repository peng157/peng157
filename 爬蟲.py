import requests
from bs4 import BeautifulSoup
import pyodbc

# 使用 Windows 驗證連接 SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=LUCAS\\SQLEXPRESS;'
                      'DATABASE=PTT八卦;'
                      'Trusted_Connection=yes')
cursor = conn.cursor()

# 建立資料表（如果不存在）
cursor.execute('''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name=N'gossiping' AND xtype='U')
BEGIN
    CREATE TABLE gossiping (
        id INT PRIMARY KEY IDENTITY(1,1),
        title NVARCHAR(255),
        link NVARCHAR(255),
        date NVARCHAR(50),
        pop NVARCHAR(50)
    )
END
''')
conn.commit()

def getData(url):
    headers = {
        'cookie': 'over18=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.find_all('div', class_='title')
    dates = soup.find_all('div', class_='date')
    nrecs = soup.find_all('div', class_='nrec')

    for i in range(len(titles)):
        title = titles[i]
        date = dates[i]
        nrec = nrecs[i]

        # 標題
        if title.a is not None:
            title_text = title.a.text.strip()
            link = f"https://www.ptt.cc{title.a['href']}"
        else:
            title_text = "無"
            link = "無"

        # 日期
        date_text = date.text.strip()

        # 人氣（pop）
        pop_text = nrec.text.strip() if nrec.text.strip() != '' else "無"

        # 插入資料
        cursor.execute('''
        INSERT INTO gossiping (title, link, date, pop)
        VALUES (?, ?, ?, ?)
        ''', (title_text, link, date_text, pop_text))

    nextLink = soup.find('a', string='‹ 上頁')
    return nextLink['href']

def ppt_八卦():
    n = int(input('請輸入想爬取幾頁: '))
    pageurl = 'https://www.ptt.cc/bbs/Gossiping/index.html'
    count = 1

    while count <= n:
        print(f'第 {count} 頁')
        next_page = getData(pageurl)
        pageurl = 'https://www.ptt.cc' + next_page
        count += 1

    conn.commit()
    print("資料已儲存至 SQL Server 資料庫")
    conn.close()

if __name__ == '__main__':
    ppt_八卦()
