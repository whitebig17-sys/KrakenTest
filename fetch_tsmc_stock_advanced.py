"""
台積電股價爬蟲程序（進階版本）
支持定時爬取、價格警報和數據庫存儲
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import os
import json
import schedule
import time
from pathlib import Path

# 配置參數
CONFIG = {
    'output_dir': r'C:\tsmc',
    'tsmc_ticker': '2330.TW',
    'check_interval': 300,  # 每5分鐘檢查一次（秒）
    'price_alert_threshold': 0.05,  # 價格變化5%時發出警告
    'historical_period': '3mo',  # 歷史數據時間跨度
}

class TSMCStockFetcher:
    """台積電股票數據爬蟲類"""
    
    def __init__(self, config=None):
        """初始化爬蟲"""
        self.config = config or CONFIG
        self.output_dir = Path(self.config['output_dir'])
        self.ticker = self.config['tsmc_ticker']
        self.last_price = None
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """確保輸出目錄存在"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ 輸出目錄: {self.output_dir}")
    
    def fetch_current_price(self):
        """獲取當前股票價格"""
        try:
            tsmc = yf.Ticker(self.ticker)
            data = tsmc.info
            
            price_data = {
                'ticker': self.ticker,
                'name': data.get('longName', 'TSMC'),
                'current_price': data.get('currentPrice', data.get('regularMarketPrice', 'N/A')),
                'currency': data.get('currency', 'TWD'),
                'previous_close': data.get('previousClose', 'N/A'),
                'open': data.get('open', 'N/A'),
                'bid': data.get('bid', 'N/A'),
                'ask': data.get('ask', 'N/A'),
                'day_high': data.get('dayHigh', 'N/A'),
                'day_low': data.get('dayLow', 'N/A'),
                'volume': data.get('volume', 'N/A'),
                'market_cap': data.get('marketCap', 'N/A'),
                'pe_ratio': data.get('trailingPE', 'N/A'),
                'dividend_yield': data.get('dividendYield', 'N/A'),
                'timestamp': datetime.now().isoformat()
            }
            return price_data
        except Exception as e:
            print(f"❌ 錯誤: 無法獲取股票數據 - {e}")
            return None
    
    def fetch_historical_data(self, period=None):
        """獲取歷史股票數據"""
        period = period or self.config['historical_period']
        try:
            tsmc = yf.Ticker(self.ticker)
            hist = tsmc.history(period=period)
            return hist
        except Exception as e:
            print(f"❌ 錯誤: 無法獲取歷史數據 - {e}")
            return None
    
    def check_price_alert(self, current_price):
        """檢查價格是否超過警報閾值"""
        if self.last_price is None:
            self.last_price = current_price
            return False
        
        if isinstance(current_price, (int, float)) and isinstance(self.last_price, (int, float)):
            price_change_percent = abs(current_price - self.last_price) / self.last_price
            threshold = self.config['price_alert_threshold']
            
            if price_change_percent >= threshold:
                change = current_price - self.last_price
                return True, change, price_change_percent * 100
        
        return False, 0, 0
    
    def save_data_json(self, data, filename):
        """以JSON格式存儲數據"""
        file_path = self.output_dir / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 錯誤: 無法保存JSON文件 {filename} - {e}")
            return False
    
    def save_data_csv(self, data, filename):
        """以CSV格式存儲數據"""
        file_path = self.output_dir / filename
        try:
            if isinstance(data, pd.DataFrame):
                data.to_csv(file_path, encoding='utf-8-sig')
            else:
                df = pd.DataFrame([data])
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"❌ 錯誤: 無法保存CSV文件 {filename} - {e}")
            return False
    
    def save_current_price(self, price_data):
        """存儲當前股票價格"""
        if price_data is None:
            return False
        
        self.save_data_json(price_data, 'tsmc_current_price.json')
        self.save_data_csv(price_data, 'tsmc_current_price.csv')
        
        # 追加到歷史記錄
        self.append_to_price_log(price_data)
        return True
    
    def append_to_price_log(self, price_data):
        """將價格追加到日誌文件"""
        log_file = self.output_dir / 'tsmc_price_log.json'
        
        try:
            # 讀取現有日誌
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            # 追加新數據
            log_data.append(price_data)
            
            # 保存（最多保留1000條記錄）
            if len(log_data) > 1000:
                log_data = log_data[-1000:]
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 錯誤: 無法更新價格日誌 - {e}")
    
    def save_historical_data(self, hist_data):
        """存儲歷史股票數據"""
        if hist_data is None or hist_data.empty:
            return False
        
        self.save_data_csv(hist_data, 'tsmc_historical_data.csv')
        
        # 保存為JSON
        hist_dict = hist_data.reset_index().to_dict(orient='records')
        for record in hist_dict:
            record['Date'] = record['Date'].isoformat() if hasattr(record['Date'], 'isoformat') else str(record['Date'])
        
        self.save_data_json(hist_dict, 'tsmc_historical_data.json')
        return True
    
    def display_price_info(self, price_data):
        """顯示股票價格信息"""
        if price_data is None:
            return
        
        print("\n" + "="*60)
        print(f"📊 台積電 ({price_data['ticker']}) 股票信息")
        print("="*60)
        print(f"公司名稱: {price_data['name']}")
        print(f"當前價格: {price_data['current_price']} {price_data['currency']}")
        print(f"前收價: {price_data['previous_close']}")
        print(f"開盤價: {price_data['open']}")
        print(f"買價: {price_data['bid']} / 賣價: {price_data['ask']}")
        print(f"日最高: {price_data['day_high']} / 日最低: {price_data['day_low']}")
        print(f"成交量: {price_data['volume']}")
        print(f"市值: {price_data['market_cap']}")
        print(f"本益比: {price_data['pe_ratio']}")
        print(f"股息殖利率: {price_data['dividend_yield']}")
        print(f"更新時間: {price_data['timestamp']}")
        print("="*60 + "\n")
    
    def run_once(self):
        """運行一次爬蟲"""
        print(f"\n🔄 開始爬蟲任務 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
        # 獲取當前價格
        current_price = self.fetch_current_price()
        if current_price:
            self.display_price_info(current_price)
            self.save_current_price(current_price)
            
            # 檢查價格警報
            alert, change, change_percent = self.check_price_alert(current_price['current_price'])
            if alert:
                print(f"⚠️  價格警報: 價格變化 {change:+.2f} ({change_percent:+.2f}%)")
            
            self.last_price = current_price['current_price']
        
        # 獲取歷史數據
        historical_data = self.fetch_historical_data()
        if historical_data is not None and not historical_data.empty:
            print(f"✓ 已獲取 {len(historical_data)} 天的歷史數據")
            self.save_historical_data(historical_data)
        
        print(f"✓ 爬蟲任務完成，數據已存儲到 {self.output_dir}")
    
    def schedule_periodic_fetch(self, interval_seconds=None):
        """定時爬蟲"""
        interval_seconds = interval_seconds or self.config['check_interval']
        
        print(f"\n🔔 啟動定時爬蟲 (間隔: {interval_seconds}秒)")
        print("按 Ctrl+C 停止\n")
        
        # 立即運行一次
        self.run_once()
        
        # 定時任務
        schedule.every(interval_seconds).seconds.do(self.run_once)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分鐘檢查一次排程
        except KeyboardInterrupt:
            print("\n\n🛑 爬蟲已停止")

def main():
    """主程序"""
    print("="*60)
    print("台積電股價爬蟲程序（進階版本）")
    print("="*60)
    
    fetcher = TSMCStockFetcher()
    
    print("\n請選擇操作模式:")
    print("1. 運行一次")
    print("2. 定時爬蟲（每5分鐘）")
    print("3. 自定義間隔")
    
    choice = input("\n請輸入選項 (1/2/3): ").strip()
    
    if choice == '1':
        fetcher.run_once()
    elif choice == '2':
        fetcher.schedule_periodic_fetch()
    elif choice == '3':
        try:
            interval = int(input("請輸入間隔時間（秒）: "))
            fetcher.schedule_periodic_fetch(interval)
        except ValueError:
            print("❌ 無效的輸入")
    else:
        print("❌ 無效的選項，運行一次")
        fetcher.run_once()

if __name__ == "__main__":
    main()
