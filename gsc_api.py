import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSearchConsoleAPI:
    def __init__(self, credentials_path):
        """Google Search Console API の認証を行い、API クライアントを初期化"""
        self.credentials_path = credentials_path
        self.service = self.authenticate()

    def authenticate(self):
        """Google Search Console API に認証する"""
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path,
            scopes=["https://www.googleapis.com/auth/webmasters"]
        )
        service = build("searchconsole", "v1", credentials=credentials)
        return service

    def get_sites(self):
        """Search Console に登録されているサイトの一覧を取得"""
        sites = self.service.sites().list().execute()
        return [site["siteUrl"] for site in sites.get("siteEntry", [])]

    def get_search_performance(self, site_url, start_date, end_date, dimensions=["query"], row_limit=10):
        """検索パフォーマンスのデータを取得"""
        request = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": row_limit
        }
        response = self.service.searchanalytics().query(siteUrl=site_url, body=request).execute()
        return response.get("rows", [])

    def submit_sitemap(self, site_url, sitemap_url):
        """サイトマップを送信"""
        response = self.service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        return response

    def get_index_coverage(self, site_url):
        """インデックスカバレッジのデータを取得"""
        response = self.service.urlInspection().index(body={"siteUrl": site_url})
        return response

    def inspect_url(self, site_url, url):
        """特定のURLを調査"""
        request = {
            "inspectionUrl": url,
            "siteUrl": site_url
        }
        response = self.service.urlInspection().index().inspect(body=request).execute()
        return response

# 例: 実行
if __name__ == "__main__":
    credentials_file = "indexing-api-447205-ca69b1d45533.json"
    gsc_api = GoogleSearchConsoleAPI(credentials_file)

    # サイト一覧を取得
    sites = gsc_api.get_sites()
    print("登録されているサイト一覧:", sites)

    if sites:
        site_url = sites[0]

        # 検索パフォーマンスデータを取得
        performance_data = gsc_api.get_search_performance(site_url, "2024-01-01", "2024-01-07")
        print("検索パフォーマンス:", performance_data)

        # サイトマップを送信
        sitemap_url = "https://example.com/sitemap.xml"
        sitemap_response = gsc_api.submit_sitemap(site_url, sitemap_url)
        print("サイトマップ送信結果:", sitemap_response)

        # インデックスカバレッジを取得
        index_coverage = gsc_api.get_index_coverage(site_url)
        print("インデックスカバレッジ:", index_coverage)

        # 特定URLの調査
        test_url = "https://example.com/test-page"
        url_inspection = gsc_api.inspect_url(site_url, test_url)
        print("URLインスペクション:", url_inspection)