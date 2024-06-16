import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class WebScraper:
    def create_directory(self, directory, company_name):
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(directory + "/" + company_name)
        elif not os.path.exists(directory + "/" + company_name):
            os.makedirs(directory + "/" + company_name)

    def save_document(self, content, path, mode="w"):
        with open(path, mode, encoding="utf-8") as file:
            file.write(content)

    def get_links(self, base_url, soup):
        links = set()
        for anchor in soup.find_all("a", href=True):
            link = anchor["href"]
            full_link = urljoin(base_url, link)
            links.add(full_link)
        return links

    def crawl_website(
        self, base_url, save_directory, error_directory, company_name, max_depth=4
    ):
        if not company_name:
            company_name = base_url

        crawledFilename = os.path.join(
            error_directory,
            company_name,
            "crawled.txt",
        )

        self.create_directory(save_directory, company_name)
        self.create_directory(error_directory, company_name)

        visited = set()
        to_visit = [(base_url, 0)]

        while to_visit:
            url, depth = to_visit.pop()
            if depth > max_depth or url in visited:
                continue

            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {e}")
                errorFilename = os.path.join(
                    error_directory,
                    company_name,
                    "errors.txt",
                )
                self.save_document(url + "\n", errorFilename, "a")
                continue

            visited.add(url)
            soup = BeautifulSoup(response.text, "html.parser")

            for data in soup(["style", "script", "img"]):
                # Remove tags
                data.decompose()

            extracted_text = " ".join(soup.stripped_strings)

            # Save the document
            filename = os.path.join(
                save_directory,
                company_name,
                url.replace(base_url, "").strip("/").replace("/", "_") + ".txt",
            )
            self.save_document(extracted_text, filename, "w")
            self.save_document(filename + "\n", crawledFilename, "a")
            print(f"Saved: {filename}")

            if depth < max_depth:
                links = self.get_links(base_url, soup)
                for link in links:
                    if link.startswith(base_url):
                        to_visit.append((link, depth + 1))
