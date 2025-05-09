import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 設定字型以支援中文顯示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 設定字型為 SimHei，支援中文顯示
matplotlib.rcParams['axes.unicode_minus'] = False  # 確保負號可以正確顯示

# 連接到 SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=LUCAS\SQLEXPRESS;'
                      'DATABASE=PTT八卦;'
                      'Trusted_Connection=yes')

# 讀取資料
df = pd.read_sql("SELECT * FROM gossiping", conn)

# 關閉資料庫連線
conn.close()

# 檢查 "pop" 欄位中的唯一值
print(df['pop'].unique())

# 清理 "pop" 欄位，去除多餘的空格
df['pop'] = df['pop'].str.strip()

# 統計 "爆" 和 "無" 的數量
popular_count = (df['pop'] == '爆').sum()  # 計算 "爆" 的數量
no_comments_count = (df['pop'] == '無').sum()  # 計算 "無" 的數量

# 計算其他類別的數量（排除 "爆" 和 "無"）
other_count = len(df) - popular_count - no_comments_count  # 剩下的資料算為其他類別

# 顯示各類型數量
print(f'Popular count: {popular_count}')  # 顯示 "爆" 的數量
print(f'No comments count: {no_comments_count}')  # 顯示 "無" 的數量
print(f'Other count: {other_count}')  # 顯示其他類別的數量

# 繪製圓餅圖
labels = ['Popular', 'No comments', 'Other']  # 圓餅圖的標籤
sizes = [popular_count, no_comments_count, other_count]  # 每個類別的數量

# 繪製圓餅圖並顯示百分比
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Gossip Board Popularity Statistics')  # 圖表標題
plt.axis('equal')  # 保持圓形比例
plt.show()
