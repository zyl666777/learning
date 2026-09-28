# 01 Python 分析程式（命令列版）

![第一步流程圖卡](image/01-crawler-flow.svg)

## 這一步的目標

輸入一個關鍵字，程式自動找出 Google 前 5 名的網頁，逐一分析後算出「機會分數」，判斷這個題目值不值得寫。先不做介面、資料庫和 Docker，只確認核心邏輯是對的。

## 做了什麼

| 檔案 | 負責的事 |
| --- | --- |
| `analyzer/serp.py` | 透過 Serper API 取得前 5 名；沒有金鑰時回傳示範資料 |
| `analyzer/crawler.py` | 抓取單一網頁，算出字數、找出發布或更新日期 |
| `analyzer/scoring.py` | 依規則替每筆結果加分，並彙整成一個關鍵字的總分 |
| `main.py` | 串起整個流程，把結果印在終端機 |

執行方式：

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env        # 想用真實資料再填入 SERPER_API_KEY
python main.py "seo 是什麼" "search console 教學"
```

## 為什麼這樣做

**不直接爬 Google 搜尋結果頁。** 直接爬違反 Google 的使用條款，很快就會遇到機器人驗證。Google 原本的 Custom Search JSON API 也已停止開放新客戶申請，所以改用第三方 SERP API。

**拆成三個模組。** 搜尋、抓網頁、計分是三件獨立的事，拆開之後，換 API 供應商只要改 `serp.py`，調整計分規則只要改 `scoring.py`。之後接 FastAPI 時，這三個模組可以直接重複使用。

**加入示範模式。** 沒有金鑰也能跑，別人 clone 下來就能看到效果，自己開發時也不會一直消耗 API 額度。

## 遇到的問題

- 問題：（例）抓回來的中文網頁變成亂碼
- 原因：網站沒有正確宣告編碼，requests 猜錯了
- 解法：設定 `resp.encoding = resp.apparent_encoding`，讓它依內容判斷編碼

- 問題：（例）日期明明在網頁上，卻抓不到
- 原因：計算字數時會刪掉 `<header>` 區塊，日期剛好放在裡面
- 解法：先找日期，再計算字數

（這一段請換成你實際遇到的狀況，邊做邊記）

## 學到的概念

**robots.txt 是什麼？** 可以把它想成網站門口貼的告示，寫著「哪些房間歡迎參觀、哪些請勿進入」。它沒有強制力，但守規矩的爬蟲都會先看告示再進門。

**為什麼中文字數要另外算？** 英文用空白分隔單字，數空白就知道有幾個字；中文字與字之間沒有空白，所以改成一個中文字算一個字，英文和數字則以連續的一串算一個字。

## 參考資料

- Requests 官方文件：https://requests.readthedocs.io/
- Beautiful Soup 官方文件：https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Python `urllib.robotparser`：https://docs.python.org/3/library/urllib.robotparser.html
- Serper API：https://serper.dev/
