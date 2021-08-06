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
    content = find_element(page, lambda elem: elem._element.get('class') == ['content'])
    assert content._element_name() == 'div'
    assert content._element_class() == ['content']
    assert content.is_inline == False
    assert content.is_paragraph == False
    assert len(content.children) == 3

    for p in content.children:
        assert p.is_paragraph == True
        assert p.is_inline == False


def test_inspection_ignored():
    html = """
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum <b>Xyz</b>xx</h2>
            <p>Lorem <i>ipsum</i> dolor <span>sit </span>amet.</p>
            <div><p>Mauris non mauris in est.</p></div>
            <button>Submit</button>
        </div>
    </div>
    """

    page = inspect(html)
    content = find_element(page, lambda elem: elem._element.get('class') == ['content'])
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


def test_pre_inspection():
    html = """
    <div class="content-wrapper">
        <div class="content">
            <h2>Lorem Ipsum</h2>
            <p>Lorem ipsum dolor sit amet.</p>
<pre><span class="pl-k">const</span> <span class="pl-s1">chrono</span> <span class="pl-c1">=</span> <span class="pl-en">require</span><span class="pl-kos">(</span><span class="pl-s">'chrono-node'</span><span class="pl-kos">)</span><span class="pl-kos">;</span>

<span class="pl-c">// or `import chrono from 'chrono-node'` for ECMAScript</span></pre>
            <p>Mauris non mauris.<br> in est.</p>
        </div>
    </div>
    """

    page = inspect(html)
    content = find_element(page, lambda elem: elem._element.get('class') == ['content'])

    assert len(content.children) == 4

    assert content.children[2].is_paragraph()
    assert "const chrono = require('chrono-node');" in content.children[2].get_formatted_text()

