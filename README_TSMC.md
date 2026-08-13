# 台積電股價爬蟲程序

這是一個用Python編寫的爬蟲程序，用於獲取台積電（TSMC）的實時股票價格和歷史數據。

## 功能特性

✅ 獲取台積電當前股票價格  
✅ 獲取歷史股票數據（過去一個月）  
✅ 以 JSON 和 CSV 格式存儲數據  
✅ 自動創建輸出目錄（C:\tsmc）  
✅ 詳細的股票信息展示  

## 安裝步驟

### 1. 安裝依賴包

打開終端/命令提示符，運行以下命令：

```bash
pip install -r requirements.txt
```

或逐個安裝：

```bash
pip install yfinance pandas requests
```

### 2. 運行程序

```bash
python fetch_tsmc_stock.py
```

## 輸出文件

程序會在 `C:\tsmc` 目錄下生成以下文件：

- **tsmc_current_price.json** - 當前股票價格（JSON格式）
- **tsmc_current_price.csv** - 當前股票價格（CSV格式）
- **tsmc_historical_data.json** - 歷史數據（JSON格式）
- **tsmc_historical_data.csv** - 歷史數據（CSV格式）

## 程序輸出信息

程序運行時會顯示以下信息：

- 當前股票價格
- 前收價、開盤價
- 買賣價格
- 日最高/最低價
- 市值
- 更新時間戳

## 數據說明

### 當前價格數據字段

- `ticker` - 股票代碼（2330.TW）
- `name` - 公司名稱（TSMC）
- `current_price` - 當前價格
- `currency` - 幣種（新台幣 TWD）
- `previous_close` - 前收價
- `open` - 開盤價
- `bid` - 買價
- `ask` - 賣價
- `day_high` - 日最高價
- `day_low` - 日最低價
- `market_cap` - 市值
- `timestamp` - 更新時間

### 歷史數據字段

- `Date` - 日期
- `Open` - 開盤價
- `High` - 最高價
- `Low` - 最低價
- `Close` - 收盤價
- `Volume` - 成交量
- `Dividends` - 股息
- `Stock Splits` - 股票分割

## 自定義選項

您可以修改 `fetch_tsmc_stock.py` 中的以下參數：

```python
# 修改歷史數據時間跨度
historical_data = fetch_tsmc_historical_data(period='3mo')  # 3個月
historical_data = fetch_tsmc_historical_data(period='1y')   # 1年
```

可用的時間跨度：
- `1d` - 1天
- `5d` - 5天
- `1mo` - 1個月
- `3mo` - 3個月
- `6mo` - 6個月
- `1y` - 1年
- `2y` - 2年
- `5y` - 5年
- `10y` - 10年
- `ytd` - 今年以來
- `max` - 最大範圍

## 定時爬取（可選）

如果要定時爬取股票數據，可以使用以下方法：

### 方法1：使用 `schedule` 庫

安裝：
```bash
pip install schedule
```

創建 `scheduled_fetch.py` 文件：

```python
import schedule
import time
from fetch_tsmc_stock import main

# 每天上午9點執行
schedule.every().day.at("09:00").do(main)

# 每小時執行一次
schedule.every().hour.do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
```

運行：
```bash
python scheduled_fetch.py
```

### 方法2：使用 Windows 任務排程器

1. 打開「工作排程器」
2. 創建基本工作
3. 設定觸發器（每天/每小時）
4. 動作選擇「啟動程式」
5. 程式：`python.exe`
6. 引數：`C:\Proj\KrakenTest\fetch_tsmc_stock.py`

## 故障排除

### 問題1：無法連接到網絡
確保您的網絡連接正常。yfinance 需要從雅虎財經服務器獲取數據。

### 問題2：找不到模塊
確保所有依賴包都已正確安裝：
```bash
pip install -r requirements.txt
```

### 問題3：C:\tsmc 目錄無法創建
確保您有對 C:\ 驅動器的寫入權限。如果沒有，修改程序中的 `OUTPUT_DIR` 路徑。

## 注意事項

1. **更新頻率**：股票數據在市場開盤期間每分鐘更新一次
2. **數據延遲**：實時數據可能有 15-20 分鐘的延遲
3. **時區**：所有時間戳都基於本地系統時間
4. **台灣股市交易時間**：星期一到星期五 09:00-13:30

## 進階用法

修改 `fetch_tsmc_stock.py` 以支持多個股票、郵件通知等功能。

## 許可證

MIT

## 作者

Created with Python & yfinance

---

**最後更新**: 2024年
