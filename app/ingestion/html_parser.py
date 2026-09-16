class HTMLParser:

    def parse(self, soup):
        main = (
            soup.find("main")
            or soup.find("article")
            or soup.body
        )

        if main is None:
            return []

        elements = []

        for tag in main.find_all(
            ["h1", "h2", "h3", "p", "pre", "ul", "ol"]
        ):
            text = tag.get_text(
                " ",
                strip=True
            )

            if not text:
                continue

            elements.append({
                "type": tag.name,
                "text": text
            })

        return elements