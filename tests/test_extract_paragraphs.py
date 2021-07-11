from bs4 import Tag

from kiji.inspection import inspect
from kiji.extraction import extract_content_element, extract_paragraph_elements


def test_extract_paragraphs_basic():
    page_inspection = inspect("""
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.</p>
            <p>Mauris non mauris in est pellentesque egestas ullamcorper eu magna.<br> Ut faucibus tempus dolor vel efficitur.</p>
        </div>
    </div>
    """)

    content_elem = extract_content_element(page_inspection)
    assert content_elem
    assert content_elem._element_class() == ['content']

    paragraph_elem = extract_paragraph_elements(content_elem)
    assert len(paragraph_elem) == 2

    assert 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' in paragraph_elem[0].get_formatted_text()
    assert 'Mauris non mauris in est pellentesque egestas ' in paragraph_elem[1].get_formatted_text()



