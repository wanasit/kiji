# Kiji

Kiji (記事, Article) is a library for parsing webpage or articles into clean text.


### Install

```bash
pip install kiji
```

### Usage

```python
import kiji

article = kiji.from_url('https://towardsdatascience.com/how-japanese-tokenizers-work-87ab6b256984')
paragraphs = article.get_paragraphs()

print(paragraphs[0])
# > I recently have been working on Kotori and doing...
```
