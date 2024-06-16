from WebScraper import WebScraper

website_url = "https://marutisuzuki.com"
download_folder = "downloads"
error_directory = "error"
company_name = "marutisuzuki"

scraper = WebScraper()
scraper.crawl_website(website_url, download_folder, error_directory, company_name)
