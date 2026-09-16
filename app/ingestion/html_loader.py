from pathlib import Path

from app.models.document import Document


class HTMLLoader:

    def __init__(self, docs_dir="data/raw/pytorch_docs/2.14"):
        self.docs_dir = Path(docs_dir)

    def load(self):
        documents = []

        for path in self.docs_dir.rglob("*.html"):
            html = path.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            documents.append(
                Document(
                    source=str(path.relative_to(self.docs_dir)),
                    title=path.stem,
                    html=html
                )
            )

        return documents