from kiji.inspection import inspect, inspect_file, find_element, InspectedElement


def test_basic_inspection():
    html = """
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum <b>Xyz</b>xx</h2>
            <p>Lorem <i>ipsum</i> dolor <span>sit </span>amet.</p>
            <p>Mauris non mauris in est.</p>
        </div>
    </div>
    """

    page = inspect(html)
    assert page.is_inline == False
    assert page.is_paragraph == False
    assert len(page.children) == 1

    content_wrapper: InspectedElement = page.children[0]
    assert content_wrapper.is_inline == False
    assert content_wrapper.is_paragraph == False
    assert content_wrapper._element_name() == 'div'
    assert content_wrapper._element_class() == ['content-wrapper']
    assert len(content_wrapper.children) == 1

    content: InspectedElement = content_wrapper.children[0]
    assert content._element_name() == 'div'
    assert content._element_class() == ['content']
    assert content.is_inline == False
    assert content.is_paragraph == False
    assert len(content.children) == 3

    for p in content.children:
        assert p.is_paragraph == True
        assert p.is_inline == False


def test_text_format():
    html = """
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum <b>Xyz</b>xx</h2>
            <p>Lorem <i>ipsum</i> dolor <span>sit </span>amet.</p>
            <p>Mauris non mauris.<br> in est.</p>
        </div>
    </div>
    """

    page = inspect(html)
    content = find_element(page, lambda elem: elem._element.get('class') == ['content'])

    assert len(content.children) == 3
    assert content.children[0].get_formatted_text() == 'Lorem Ipsum Xyzxx'
    assert content.children[1].get_formatted_text() == 'Lorem ipsum dolor sit amet.'
    assert content.children[2].get_formatted_text() == 'Mauris non mauris.\n in est.'

    format_text = content.get_formatted_text()
    assert 'Lorem Ipsum Xyzxx' in format_text
    assert 'Lorem ipsum dolor sit amet.' in format_text
    assert 'Mauris non mauris' in format_text


def test_html_format():
    html = """
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum <b>Xyz</b>xx</h2>
            <p>Lorem <i>ipsum</i> dolor <span>sit </span>amet.</p>
            <p>Mauris non mauris.<br> in est.</p>
        </div>
    </div>
    """

    page = inspect(html)
    content = find_element(page, lambda elem: elem._element.get('class') == ['content'])

    assert len(content.children) == 3
    assert content.children[0].get_formatted_html() == '<h2>Lorem Ipsum <b>Xyz</b>xx</h2>'
    assert content.children[1].get_formatted_html() == '<p>Lorem <i>ipsum</i> dolor <span>sit </span>amet.</p>'
    assert content.children[2].get_formatted_html() == '<p>Mauris non mauris.<br/> in est.</p>'

    format_html = content.get_formatted_html()
    assert '<h2>Lorem Ipsum <b>Xyz</b>xx</h2>' in format_html
    assert '<p>Lorem <i>ipsum</i> dolor <span>sit </span>amet.</p>' in format_html
    assert '<p>Mauris non mauris.<br/> in est.</p>' in format_html
