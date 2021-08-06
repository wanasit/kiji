import os
import kiji


def from_file(path):
    current_dir = os.path.dirname(__file__)
    return kiji.from_file(os.path.join(current_dir, path))


def test_saved_medium():
    # https://towardsdatascience.com/how-japanese-tokenizers-work-87ab6b256984
    article = from_file('saved_pages/medium-2021-06-12.html')
    paragraphs = article.get_paragraphs()

    assert 'Tokenization, or breaking a text into a list of words, is an important step' in paragraphs[0].text
    assert 'Most Japanese tokenizers use Lattice-based tokenization. ' in paragraphs[1].text


def test_saved_github():
    # https://github.com/wanasit/chrono
    article = from_file('saved_pages/github-2021-06-14.html')
    paragraphs = article.get_paragraphs()

    # Check main content extraction
    assert article.content_element._element_name() == 'article'
    assert 'markdown-body' in article.content_element._element_class()

    # Check paragraph extraction
    assert 'A natural language date parser in Javascript' in paragraphs[0].text


def test_saved_bloggie():
    # https://bloggie.io/@wanasit/implementing-and-debugging-binary-search
    article = from_file('saved_pages/bloggie-2021-06-18.html')
    paragraphs = article.get_paragraphs()

    assert 'Almost every programmer knows binary search. It’s often one of the first things we ' in paragraphs[0].text
    assert 'In this article, I want to look into an' in paragraphs[1].text
    assert 'There are other articles out there on how to write binary search correctly. Most of' in paragraphs[2].text


def test_hugging_face():
    # https://huggingface.co/transformers/task_summary.html
    article = from_file('saved_pages/huggingface-2021-08-01.html')

    paragraphs = article.get_paragraphs()

    assert 'This page shows the most frequent use-cases when using the library.' in paragraphs[0].text

    assert 'These examples leverage auto-models, which are classes that' in paragraphs[1].text
    assert 'Please check the AutoModel documentation for more information.' in paragraphs[1].text