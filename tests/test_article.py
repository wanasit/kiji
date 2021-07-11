from bs4 import Tag

from kiji import from_html


def test_basic_article():
    article = from_html("""
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum</h2>
            <p>Lorem <span class="something">ipsum dolor<span> sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.</p>
            <p>Mauris non mauris in <b>est</b> pellentesque egestas ullamcorper eu magna.<br> Ut faucibus tempus dolor vel efficitur.</p>
        </div>
    </div>
    """)

    paragraphs = article.get_paragraphs()
    assert len(paragraphs) == 2

    assert str(paragraphs[0]) == \
           'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.'
    assert str(paragraphs[1]) == \
           'Mauris non mauris in est pellentesque egestas ullamcorper eu magna.\n Ut faucibus tempus dolor vel efficitur.'

    paragraphs = article.get_paragraphs(include_headers=True)
    assert len(paragraphs) == 3

    assert str(paragraphs[0]) == 'Lorem Ipsum'
    assert str(paragraphs[1]) == \
           'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.'
    assert str(paragraphs[2]) == \
           'Mauris non mauris in est pellentesque egestas ullamcorper eu magna.\n Ut faucibus tempus dolor vel efficitur.'
