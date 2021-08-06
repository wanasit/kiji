from bs4 import Tag

from kiji.inspection import inspect, inspect_file
from kiji.extraction import extract_content_element


def test_extract_content_one_layer():
    page_inspection = inspect("""
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.</p>
            <p>Mauris non mauris in est pellentesque egestas ullamcorper eu magna. Ut faucibus tempus dolor vel efficitur.</p>
        </div>
    </div>
    """)

    content_inspection = extract_content_element(page_inspection)

    assert content_inspection
    assert content_inspection.is_element
    assert content_inspection._element_class() == ['content']

def test_extract_content_multiple_nested_sections():
    page_inspection = inspect("""
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum</h2>
            <div class="section1">
                <h2>Lorem Ipsum 1</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.</p>
            </div>
            <div class="section2">
                <h2>Lorem Ipsum 2</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ullamcorper dolor eget lacus condimentum, at laoreet neque consequat.</p>
                <p>Mauris non mauris in est pellentesque egestas ullamcorper eu magna. Ut faucibus tempus dolor vel efficitur.</p>
                <p>Mauris non mauris in est pellentesque egestas ullamcorper eu magna. Ut faucibus tempus dolor vel efficitur.</p>
                <p>Mauris non mauris in est pellentesque egestas ullamcorper eu magna. Ut faucibus tempus dolor vel efficitur.</p>
                <p>Mauris non mauris in est pellentesque egestas ullamcorper eu magna. Ut faucibus tempus dolor vel efficitur.</p>
            </div>
        </div>
    </div>
    """)

    content_inspection = extract_content_element(page_inspection)

    assert content_inspection
    assert content_inspection.is_element
    assert content_inspection._element_class() == ['content']






