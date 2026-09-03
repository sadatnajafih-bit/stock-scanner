import os
import pytse_client as tse
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="TSE Golden Cross Scanner")

# لیست نمادهای پیش‌فرض و مهم برای بررسی
SYMBOLS = [
    "فولاد", "فملی", "شستا", "شتران", "شبندر", 
    "خودرو", "خساپا", "وغدیر", "تاپیکو", "وبملت",
    "تجارت", "صبا", "نوری", "زاگرس", "پارس"
]

def analyze_symbols():
    results = []
    
    for symbol in SYMBOLS:
        try:
            ticker = tse.Ticker(symbol)
            df = ticker.history
            
            if df.empty or len(df) < 52:
                continue
                
            # مرتب‌سازی بر اساس تاریخ
            df = df.sort_index()
            
            # محاسبه میانگین متحرک ۲۰ و ۵۰ روزه
            df['MA20'] = df['close'].rolling(window=20).mean()
            df['MA50'] = df['close'].rolling(window=50).mean()
            
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            
            # تشخیص وضعیت تقاطع
            signal = "خنثی / بدون تقاطع"
            signal_color = "#6 خطای `Port Scan Timeout` مواجه نشود.
2. دریافت دیتا و محاسبات داخل درخواست (On-Demand) با مکانیزم مدیریت خطا (Try/Except) انجام می‌شود تا در صورت قطعی TSETMC کل سرور کرش نکند.
3. یک UI تمیز، راست‌چین و مدرن با فونت و استایل خوانا طراحی شده است.

کل محتوای فایل `app.py` رو پاک کن و این رو جایگزین کن:
```python
import os
import pytse_client as tse
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="TSE Golden Cross Scanner")

# لیست نمادهای پیش‌فرض و مهم برای بررسی
SYMBOLS = [
"فولاد", "فملی", "شستا", "شتران", "شبندر", 
"خودرو", "خساپا", "وغدیر", "تاپیکو", "وبملت",
"تجارت", "صبا", "نوری", "زاگرس", "پارس"
]

def analyze_symbols():
results = []

for symbol in SYMBOLS:
try:
ticker = tse.Ticker(symbol)
df = ticker.history

if df.empty or len(df) < 52:
continue

# مرتب‌سازی بر اساس تاریخ
df = df.sort_index()

# محاسبه میانگین متحرک ۲۰ و ۵۰ روزه
df['MA20'] = df['close'].rolling(window=20).mean()
df['MA50'] = df['close'].rolling(window=50).mean()

last_row = df.iloc[-1]
prev_row = df.iloc[-2]

# تشخیص وضعیت تقاطع
signal = "خنثی / بدون تقاطع"
signal_color = "#6c757d"

# گلدن کراس: قطع کردن MA50 به سمت بالا توسط MA20
if prev_row['MA20'] <= prev_row['MA50'] and last_row['MA20'] > last_row['MA50']:
signal = "🚀 گلدن کراس (سیگنال خرید قوی)"
signal_color = "#28a745"
# د</td>
<td>{item['date']}</td>
<td>{item['close']} ریال</td>
<td>{item['ma20']}</td>
<td>{item['ma50']}</td>
<td style="color: {item['color']}; font-weight: bold;">{item['signal']}</td>
</tr>
"""

if not rows_html:
rows_html = "<tr><td colspan='6'>داده‌ای دریافت نشد یا بازار در دسترس نیست. لطفاً صفحه را مجدداً رفرش کنید.</td></tr>"

html_content = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>دستیار تحلیل تکنیکال بورس (Golden Cross)</title>
<style>
body {{
font-family: Tahoma, 'Segoe UI', Arial, sans-serif;
background-color: #0f172a;
color: #e2e8f0;
margin: 0;
padding: 30px;
display: flex;
flex-direction: column;
align-items: center;
}}
.container {{
width: 95%;
max-width: 1100px;
}}
h1 {{
text-align: center;
color: #38bdf8;
margin-bottom: 10px;
}}
p.desc {{
text-align: center;
color: #94a3b8;
margin-bottom: 30px;
}}
table {{
width: 100%;
border-collapse: collapse;
background-color: #1e293b;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
border-radius: 8px;
overflow: hidden;
}}
th, td {{
padding: 14px 18px;
text-align: center;
border-bottom: 1px solid #334155;
}}
th {{
background-color: #0284c7;
color: #ffffff;
font-weight: 600;
}}
tr:hover {{
background-color: #334155;
transition: background-color 0.2s ease;
}}
.btn-refresh {{
display: inline-block;
margin-top: 25px;
padding: 10px 24px;
background-color: #0284c7;
color: white;
text-decoration: none;
border-radius: 6px;
font-weight: bold;
transition: 0.3s;
}}
.btn-refresh:hover {{
background-color: #0369a1;
}}
</style>
</head>
<body>
<div class="container">
<h1>📊 دیده‌بان تکنیکال تقاطع طلایی (Golden Cross)</h1>
<p class="desc">بررسی زنده‌ی تقاطع میانگین متحرک ۲۰ و ۵۰ روزه مستقیماً از TSETMC</p>
<table>
<thead>
<tr>
<th>نماد</th>
<th>آخرین تاریخ معامله</th>
<th>آخرین قیمت</th>
<th>MA 20</th>
<th>MA 50</th>
<th>وضعیت سیگنال</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
<div style="text-align: center;">
<a href="/" class="btn-refresh">🔄 به‌روزرسانی وضعیت نمادها</a>
</div>
</div>
</body>
</html>
"""
return html_content

if __name__ == "__main__":
port = int(os.environ.get("PORT", 10000))
uvicorn.run(app, host="0.0.0.0", port=port)

