from app.models.chunk import Chunk


class StructureChunker:

    def __init__(self, max_words=350):
        self.max_words = max_words

    def _split_text(self, text):
        words = text.split()

        if len(words) <= self.max_words:
            return [text]

        middle = len(words) // 2

        left = " ".join(words[:middle])
        right = " ".join(words[middle:])

        return (
            self._split_text(left)
            + self._split_text(right)
        )

    def chunk(self, document, elements):
        chunks = []

        headings = {
            "h1": document.title,
            "h2": "",
            "h3": ""
        }

        content = []

        def section_name():
            return " > ".join(
                value
                for value in headings.values()
                if value
            )

        def save_content():
            nonlocal content

            if not content:
                return

            current = []

            for block in content:
                block_text = block["text"]
                block_words = len(block_text.split())

                current_words = sum(
                    len(x.split())
                    for x in current
                )


                if block["type"] == "pre":
                    if current:
                        chunks.append(
                            Chunk(
                                source=document.source,
                                title=document.title,
                                section=section_name(),
                                content="\n\n".join(current)
                            )
                        )
                        current = []

                    chunks.append(
                        Chunk(
                            source=document.source,
                            title=document.title,
                            section=section_name(),
                            content=block_text
                        )
                    )

                    continue

                if current_words + block_words <= self.max_words:
                    current.append(block_text)

                else:
                    if current:
                        chunks.append(
                            Chunk(
                                source=document.source,
                                title=document.title,
                                section=section_name(),
                                content="\n\n".join(current)
                            )
                        )

                        current = []

                    for part in self._split_text(block_text):
                        current.append(part)

            if current:
                chunks.append(
                    Chunk(
                        source=document.source,
                        title=document.title,
                        section=section_name(),
                        content="\n\n".join(current)
                    )
                )

            content = []

        for element in elements:

            element_type = element["type"]

            if element_type in ["h1", "h2", "h3"]:
                save_content()

                if element_type == "h1":
                    headings["h1"] = element["text"]
                    headings["h2"] = ""
                    headings["h3"] = ""

                elif element_type == "h2":
                    headings["h2"] = element["text"]
                    headings["h3"] = ""

                elif element_type == "h3":
                    headings["h3"] = element["text"]

            else:
                content.append(element)

        save_content()

        return chunks