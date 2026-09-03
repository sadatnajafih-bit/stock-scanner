import os
from datetime import datetime
import pandas as pd
import pytse_client as tse
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Iran Stock Technical Scanner")

SYMBOLS = ["خودرو", "شپدیس", "ذوب", "سپه", "وغدیر"]

def get_close_column(df):
    for col in ["close", "Close", "adjClose", "Adj Close", "close_price", "ClosePrice"]:
        if col in df.columns:
            return col
    return None

def analyze_symbol(symbol):
    try:
        data = tse.download(symbols=symbol, write_to_csv=False, adjust=True, include_jdate=True)
        df = data.get(symbol) if isinstance(data, dict) else data

        if df is None or df.empty:
            return {"symbol": symbol, "status": "error", "message": "داده‌ای یافت نشد."}

        df = df.copy()
        col = get_close_column(df)
        if not col:
            return {"symbol": symbol, "status": "error", "message": "ستون قیمت پیدا نشد."}

        df["ClosePrice"] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["ClosePrice"])

        if not isinstance(df.index, pd.DatetimeIndex):
            try:
                df.index = pd.to_datetime(df.index)
            except Exception:
                pass
        df = df.sort_index()

        if len(df) < 50:
            return {"symbol": symbol, "status": "error", "message": f"تعداد سوابق ناکافی است: {len(df)}"}

        df["MA20"] = df["ClosePrice"].rolling(window=20).mean()
        df["MA50"] = df["ClosePrice"].rolling(window=50).mean()
        df["Spread"] = df["MA20"] - df["MA50"]
        df["PrevSpread"] = df["Spread"].shift(1)

        df["GoldenCross"] = (df["PrevSpread"] <= 0) & (df["Spread"] > 0)
        df["DeathCross"] = (df["PrevSpread"] >= 0) & (df["Spread"] < 0)

        recent_5 = df.tail(5)
        last = df.iloc[-1]

        gc = bool(recent_5["GoldenCross"].fillna(False).any())
        dc = bool(recent_5["DeathCross"].fillna(False).any())

        if gc:
            signal = "Golden Cross"
        elif dc:
            signal = "Death Cross"
        elif last["MA20"] > last["MA50"]:
            signal = "روند صعودی"
        else:
            signal = "روند نزولی"

        return {
            "symbol": symbol,
            "status": "ok",
            "last_date": str(df.index[-1]),
            "last_price": round(float(last["ClosePrice"]), 2),
            "ma20": round(float(last["MA20"]), 2),
            "ma50": round(float(last["MA50"]), 2),
            "golden_cross_last_5_days": gc,
            "death_cross_last_5_days": dc,
            "signal": signal,
        }
    except Exception as e:
        return {"symbol": symbol, "status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    results = [analyze_symbol(s) for s in SYMBOLS]
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    rows = ""
    for item in results:
        if item["status"] == "error":
            rows += f"<tr><td>{item['symbol']}</td><td colspan='7' style='color:red'>خطا: {item['message']}</td></tr>"
            continue

        color = "green" if item["signal"] == "Golden Cross" else "red" if item["signal"] == "Death Cross" else "blue" if item["signal"] == "روند صعودی" else "darkorange"
        rows += f"""
        <tr>
            <td>{item['symbol']}</td>
            <td>{item['last_date']}</td>
            <td>{item['last_price']}</td>
            <td>{item['ma20']}</td>
            <td>{item['ma50']}</td>
            <td style='color:{color}; font-weight:bold'>{item['signal']}</td>
            <td>{item['golden_cross_last_5_days']}</td>
            <td>{item['death_cross_last_5_days']}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>اسکنر بورس ایران</title>
        <style>
            body {{ font-family: Tahoma, Arial; margin: 30px; background: #f8f9fa; }}
            table {{ width: 100%; border-collapse: collapse; background: #fff; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: center; }}
            th {{ background: #343a40; color: #fff; }}
        </style>
    </head>
    <body>
        <h2>اسکنر تکنیکال بورس ایران (Golden Cross)</h2>
        <p>زمان استخراج داده: <b>{scan_time}</b></p>
        <table>
            <thead>
                <tr>
                    <th>نماد</th>
                    <th>تاریخ آخرین کندل</th>
                    <th>قیمت پایانی</th>
                    <th>MA 20</th>
                    <th>MA 50</th>
                    <th>سیگنال / وضعیت</th>
                    <th>تقاطع طلایی (۵ روز اخیر)</th>
                    <th>تقاطع مرگ (۵ روز اخیر)</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
