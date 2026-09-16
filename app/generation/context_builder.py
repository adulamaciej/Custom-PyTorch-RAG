class ContextBuilder:

    BASE_URL = "https://docs.pytorch.org/docs/stable"

    def build(self, results):
        context_parts = []
        sources = []

        for i, result in enumerate(
            results,
            start=1
        ):
            url = (
                f"{self.BASE_URL}/"
                f"{result.chunk.source}"
            )

            context_parts.append(
                f"""
SOURCE [{i}]
Section: {result.chunk.section}
URL: {url}

{result.chunk.content}
""".strip()
            )

            sources.append({
                "id": i,
                "section": result.chunk.section,
                "url": url
            })

        return (
            "\n\n---\n\n".join(context_parts),
            sources
        )