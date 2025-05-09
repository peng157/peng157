from flask import Flask, render_template
import pyodbc
import pandas as pd

app = Flask(__name__)

# 設定 SQL Server 連接
def get_data_from_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=LUCAS\\SQLEXPRESS;'
                          'DATABASE=PTT八卦;'
                          'Trusted_Connection=yes')
    df = pd.read_sql("SELECT * FROM gossiping", conn)
    conn.close()
    return df

@app.route('/')
def index():
    # 從資料庫讀取資料
    df = get_data_from_db()
    # 把資料轉成字典形式傳遞給模板
    data = df.to_dict(orient='records')
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)