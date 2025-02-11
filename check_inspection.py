import gsc_api
import csv
import time

# 認証情報ファイルのパス
credentials_path = "./indexing-api-447205-ca69b1d45533.json"

# Google Search Console API のインスタンスを作成
api = gsc_api.GoogleSearchConsoleAPI(credentials_path)

# 入力CSVファイルと出力CSVファイルのパス
input_csv = "sites.csv"
output_csv = f"inspection_results_{int(time.time())}.csv"
domain = "sc-domain:kokoshiro.jp"

# URLのインスペクションを実行し、結果をCSVに保存
def inspect_urls(input_csv, output_csv):
    with open(input_csv, "r") as infile, open(output_csv, "w", newline="") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # ヘッダーを書き込む
        writer.writerow([
            "URL", 
            "Verdict", 
            "Coverage State", 
            "Robots Txt State", 
            "Indexing State",
            "Last Crawl Time",
            "Page Fetch State",
            "Google Canonical",
            "Crawled As"
        ])
        
        for row in reader:
            url = row[0].strip()
            if not url:
                continue
            
            try:
                result = api.inspect_url(domain, url)
                index_result = result.get('inspectionResult', {}).get('indexStatusResult', {})
                
                writer.writerow([
                    url,
                    index_result.get('verdict', 'N/A'),
                    index_result.get('coverageState', 'N/A'),
                    index_result.get('robotsTxtState', 'N/A'),
                    index_result.get('indexingState', 'N/A'),
                    index_result.get('lastCrawlTime', 'N/A'),
                    index_result.get('pageFetchState', 'N/A'),
                    index_result.get('googleCanonical', 'N/A'),
                    index_result.get('crawledAs', 'N/A')
                ])
                
                # Rate Limitを考慮して少し待機
                time.sleep(1)
            except Exception as e:
                writer.writerow([url, "Error", str(e)])
                print(f"Error inspecting {url}: {e}")

# 実行
inspect_urls(input_csv, output_csv)
print(f"Inspection results saved to {output_csv}")
