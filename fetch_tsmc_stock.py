"""
台積電股價爬虫程序
抓取台積電（TSMC）實時股票價格並存儲到 C:\tsmc 文件夾
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import json

# 台積電的股票代碼
TSMC_TICKER = "2330.TW"
OUTPUT_DIR = r"C:\tsmc"

def ensure_output_directory():
    """確保輸出目錄存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"已創建目錄: {OUTPUT_DIR}")
    else:
        print(f"目錄已存在: {OUTPUT_DIR}")

def fetch_tsmc_current_price():
    """獲取台積電當前股票價格"""
    try:
        print("正在獲取台積電股票數據...")
        tsmc = yf.Ticker(TSMC_TICKER)
        
        # 獲取當前價格信息
        data = tsmc.info
        current_price = data.get('currentPrice', data.get('regularMarketPrice', 'N/A'))
        
        return {
            'ticker': TSMC_TICKER,
            'name': data.get('longName', 'TSMC'),
            'current_price': current_price,
            'currency': data.get('currency', 'TWD'),
            'previous_close': data.get('previousClose', 'N/A'),
            'open': data.get('open', 'N/A'),
            'bid': data.get('bid', 'N/A'),
            'ask': data.get('ask', 'N/A'),
            'day_high': data.get('dayHigh', 'N/A'),
            'day_low': data.get('dayLow', 'N/A'),
            'market_cap': data.get('marketCap', 'N/A'),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"錯誤: 無法獲取股票數據 - {e}")
        return None

def fetch_tsmc_historical_data(period='1mo'):
    """獲取台積電歷史股票數據"""
    try:
        print(f"正在獲取台積電過去 {period} 的歷史數據...")
        tsmc = yf.Ticker(TSMC_TICKER)
        hist = tsmc.history(period=period)
        return hist
    except Exception as e:
        print(f"錯誤: 無法獲取歷史數據 - {e}")
        return None

def save_current_price_json(price_data):
    """以 JSON 格式存儲當前股票價格"""
    if price_data is None:
        return False
    
    file_path = os.path.join(OUTPUT_DIR, 'tsmc_current_price.json')
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(price_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存當前股票數據到: {file_path}")
        return True
    except Exception as e:
        print(f"錯誤: 無法保存JSON文件 - {e}")
        return False

def save_current_price_csv(price_data):
    """以 CSV 格式存儲當前股票價格"""
    if price_data is None:
        return False
    
    file_path = os.path.join(OUTPUT_DIR, 'tsmc_current_price.csv')
    try:
        df = pd.DataFrame([price_data])
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✓ 已保存當前股票數據到: {file_path}")
        return True
    except Exception as e:
        print(f"錯誤: 無法保存CSV文件 - {e}")
        return False

def save_historical_data_csv(hist_data):
    """以 CSV 格式存儲歷史股票數據"""
    if hist_data is None or hist_data.empty:
        return False
    
    file_path = os.path.join(OUTPUT_DIR, 'tsmc_historical_data.csv')
    try:
        hist_data.to_csv(file_path, encoding='utf-8-sig')
        print(f"✓ 已保存歷史股票數據到: {file_path}")
        return True
    except Exception as e:
        print(f"錯誤: 無法保存CSV文件 - {e}")
        return False

def save_historical_data_json(hist_data):
    """以 JSON 格式存儲歷史股票數據"""
    if hist_data is None or hist_data.empty:
        return False
    
    file_path = os.path.join(OUTPUT_DIR, 'tsmc_historical_data.json')
    try:
        # 轉換為可序列化的格式
        hist_dict = hist_data.reset_index().to_dict(orient='records')
        # 將日期轉換為字符串
        for record in hist_dict:
            record['Date'] = record['Date'].isoformat() if hasattr(record['Date'], 'isoformat') else str(record['Date'])
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(hist_dict, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存歷史股票數據到: {file_path}")
        return True
    except Exception as e:
        print(f"錯誤: 無法保存JSON文件 - {e}")
        return False

def display_price_info(price_data):
    """顯示股票價格信息"""
    if price_data is None:
        return
    
    print("\n" + "="*50)
    print(f"台積電 ({price_data['ticker']}) 股票信息")
    print("="*50)
    print(f"公司名稱: {price_data['name']}")
    print(f"當前價格: {price_data['current_price']} {price_data['currency']}")
    print(f"前收價: {price_data['previous_close']}")
    print(f"開盤價: {price_data['open']}")
    print(f"買價: {price_data['bid']}")
    print(f"賣價: {price_data['ask']}")
    print(f"日最高: {price_data['day_high']}")
    print(f"日最低: {price_data['day_low']}")
    print(f"市值: {price_data['market_cap']}")
    print(f"更新時間: {price_data['timestamp']}")
    print("="*50 + "\n")

def main():
    """主程序"""
    print("台積電股價爬蟲程序啟動\n")
    
    # 確保輸出目錄存在
    ensure_output_directory()
    
    # 獲取當前股票價格
    print("\n【獲取當前股票價格】")
    current_price = fetch_tsmc_current_price()
    if current_price:
        display_price_info(current_price)
        save_current_price_json(current_price)
        save_current_price_csv(current_price)
    
    # 獲取歷史數據（過去一個月）
    print("\n【獲取歷史股票數據】")
    historical_data = fetch_tsmc_historical_data(period='1mo')
    if historical_data is not None and not historical_data.empty:
        print(f"已獲取 {len(historical_data)} 天的歷史數據")
        save_historical_data_csv(historical_data)
        save_historical_data_json(historical_data)
    
    print("\n程序完成！所有數據已保存到 C:\\tsmc 文件夾")

if __name__ == "__main__":
    main()
