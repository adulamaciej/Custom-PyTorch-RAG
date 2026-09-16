from bs4 import BeautifulSoup

from app.ingestion.html_parser import HTMLParser


def test_parser():

    html = """
    <html>
        <body>
            <main>
                <h1>Autograd</h1>
                <p>Automatic differentiation.</p>

                <h2>Example</h2>

                <pre>
                import torch
                </pre>
            </main>
        </body>
    </html>
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    parser = HTMLParser()

    elements = parser.parse(soup)

    assert elements[0]["type"] == "h1"
    assert elements[0]["text"] == "Autograd"