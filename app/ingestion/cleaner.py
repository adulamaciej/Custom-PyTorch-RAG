from bs4 import BeautifulSoup


class HTMLCleaner:

    def clean(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer"
        ]):
            tag.decompose()

        return soup