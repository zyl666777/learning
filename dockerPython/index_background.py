"""第一步：命令列版本。輸入關鍵字，印出前 5 名分析與機會分數。

用法：python main.py "seo 是什麼" "search console 教學"
"""
import sys
import time

from dotenv import load_dotenv

from analyzer.crawler import fetch_page
from analyzer.scoring import is_forum, score_result, summarize
from analyzer.serp import is_mock_mode, search_top5

REQUEST_DELAY = 1.5  # 秒；對每個網站保持禮貌


def analyze(keyword: str, mock: bool) -> dict:
    results = []
    for item in search_top5(keyword):
        page = fetch_page(item["url"], mock=mock)
        results.append({**item, **page})
        if not mock:
            time.sleep(REQUEST_DELAY)
    return {"keyword": keyword, "results": results, **summarize(results)}


def print_report(report: dict) -> None:
    print(f"\n關鍵字：{report['keyword']}")
    print(f"機會分數：{report['score']} / 100　論壇 {report['forum_count']} 筆　"
          f"平均字數 {report['avg_words'] or '—'}　最舊 {report['oldest_date'] or '—'}")
    for r in report["results"]:
        tag = "論壇" if is_forum(r["url"]) else "一般"
        if r["ok"]:
            detail = f"{r['word_count']} 字　{r['date'] or '日期不明'}"
        else:
            detail = f"無法取得（{r['error']}）"
        print(f"  {r['position']}. [{tag}] +{score_result(r):>2}　{detail}　{r['url']}")


def main() -> None:
    load_dotenv()
    keywords = sys.argv[1:]
    if not keywords:
        print('請輸入關鍵字，例如：python main.py "seo 是什麼"')
        sys.exit(1)
    mock = is_mock_mode()
    if mock:
        print("未設定 SERPER_API_KEY，使用示範模式。")
    for kw in keywords:
        print_report(analyze(kw, mock))


if __name__ == "__main__":
    main()