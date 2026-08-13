# 快速開始指南

## 第1步：安裝依賴包

打開命令提示符或PowerShell，進入項目目錄：

```bash
cd C:\Proj\KrakenTest
pip install -r requirements.txt
```

## 第2步：選擇版本運行

### 方式1：基礎版本（推薦初次使用）

```bash
python fetch_tsmc_stock.py
```

**功能：**
- ✅ 獲取當前股票價格
- ✅ 獲取過去一個月的歷史數據
- ✅ 將數據存儲到 C:\tsmc 文件夾
- ✅ 支持 JSON 和 CSV 格式

**生成的文件：**
- `tsmc_current_price.json` - 當前價格（JSON）
- `tsmc_current_price.csv` - 當前價格（CSV）
- `tsmc_historical_data.json` - 歷史數據（JSON）
- `tsmc_historical_data.csv` - 歷史數據（CSV）

---

### 方式2：進階版本（支持定時爬蟲）

```bash
python fetch_tsmc_stock_advanced.py
```

**功能：**
- ✅ 所有基礎版本功能
- ✅ 支持定時自動爬蟲
- ✅ 價格變化警報
- ✅ 價格歷史日誌（tsmc_price_log.json）
- ✅ 更詳細的股票信息（本益比、股息殖利率等）

**使用選項：**
- 選項1: 運行一次
- 選項2: 定時爬蟲（每5分鐘自動更新）
- 選項3: 自定義間隔時間

---

## 第3步：檢查輸出

程序運行後，檢查 `C:\tsmc` 文件夾中的輸出文件：

```bash
dir C:\tsmc
```

## 文件說明

### 當前價格文件格式

**JSON 格式（tsmc_current_price.json）：**
```json
{
  "ticker": "2330.TW",
  "name": "Taiwan Semiconductor Manufacturing Company Limited",
  "current_price": 620.5,
  "currency": "TWD",
  "previous_close": 618.0,
  "open": 621.0,
  "bid": 620.4,
  "ask": 620.6,
  "day_high": 625.0,
  "day_low": 618.0,
  "market_cap": 23456789000000,
  "timestamp": "2024-08-13T10:30:45.123456"
}
```

**CSV 格式（tsmc_current_price.csv）：**
```
ticker,name,current_price,currency,previous_close,open,...
2330.TW,TSMC,620.5,TWD,618.0,621.0,...
```

---

## 常見問題

### Q: 為什麼無法創建 C:\tsmc 文件夾？
**A:** 確保您有對 C:\ 驅動器的寫入權限。如果沒有，可以：
1. 以管理員身份運行命令提示符
2. 或修改程序中的 `OUTPUT_DIR` 路徑到有權限的位置

### Q: 如何修改輸出位置？
**A:** 編輯 Python 文件中的 `OUTPUT_DIR` 或 `config` 字典：

```python
# 基礎版本 - 修改這一行
OUTPUT_DIR = r"D:\MyData\TSMC"

# 進階版本 - 修改配置
CONFIG = {
    'output_dir': r"D:\MyData\TSMC",
    ...
}
```

### Q: 如何修改爬蟲間隔時間？
**A:** 編輯進階版本中的配置：

```python
CONFIG = {
    ...
    'check_interval': 300,  # 改為 600 表示10分鐘
}
```

### Q: 如何只獲取特定時間段的歷史數據？
**A:** 修改程序中的時間跨度參數：

```python
# 基礎版本
historical_data = fetch_tsmc_historical_data(period='1y')  # 改為1年

# 進階版本
CONFIG = {
    ...
    'historical_period': '6mo',  # 改為6個月
}
```

### Q: 股票代碼能改成其他股票嗎？
**A:** 可以。修改代碼中的 `TSMC_TICKER` 或 `tsmc_ticker`：

```python
# 改成其他台灣股票
'tsmc_ticker': '2330.TW'  # 台積電
'tsmc_ticker': '2454.TW'  # 聯發科
'tsmc_ticker': '2330'     # 台灣交易所代碼

# 或國際股票
'tsmc_ticker': 'AAPL'     # 蘋果
'tsmc_ticker': 'TSLA'     # 特斯拉
```

---

## 進階用法

### 1. 定時任務 + Windows 任務排程

創建批處理文件 `run_tsmc.bat`：
```batch
@echo off
cd C:\Proj\KrakenTest
python fetch_tsmc_stock.py
```

然後在 Windows 任務排程器中設定每日運行。

### 2. 多個股票同時監控

修改程序以支持多個股票列表。

### 3. 與數據庫集成

將數據存儲到 SQLite、MySQL 等數據庫。

### 4. 發送郵件通知

當價格超過閾值時發送郵件警報。

---

## 數據備份

建議定期備份 C:\tsmc 文件夾中的數據：

```bash
# 使用 PowerShell 備份
Copy-Item -Path "C:\tsmc" -Destination "D:\Backups\tsmc_backup_$(Get-Date -Format 'yyyyMMdd')" -Recurse
```

---

## 完成！

現在你已經有一個完整的台積電股價爬蟲程序了！

更多詳細信息請參考 `README_TSMC.md`
