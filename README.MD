# package
BeautifulSoup 4
pandas 
requests
lxml
numpy

# CkipTagger
#### GitHub

https://github.com/ckiplab/ckiptagger

[![GitHub release](https://img.shields.io/github/v/release/ckiplab/ckiptagger.svg?maxAge=3600)](https://github.com/ckiplab/ckiptagger/releases)
[![GitHub release date](https://img.shields.io/github/release-date/ckiplab/ckiptagger.svg?maxAge=3600)](https://github.com/ckiplab/ckiptagger/releases)
[![GitHub issues](https://img.shields.io/github/issues/ckiplab/ckiptagger.svg?maxAge=3600)](https://github.com/ckiplab/ckiptagger/issues)

#### PyPI

https://pypi.org/project/ckiptagger

[![PyPI version](https://img.shields.io/pypi/v/ckiptagger.svg?maxAge=3600)](https://pypi.org/project/ckiptagger)
[![PyPI license](https://img.shields.io/pypi/l/ckiptagger.svg?maxAge=3600)](https://github.com/ckiplab/ckiptagger/blob/master/LICENSE)
[![PyPI python](https://img.shields.io/pypi/pyversions/ckiptagger.svg?maxAge=3600)](https://pypi.org/project/ckiptagger)

#### Documentation

https://github.com/ckiplab/ckiptagger/wiki

#### Author / Maintainers

[Peng-Hsuan Li](https://jacobvsdanniel.github.io)@[CKIP](http://ckip.iis.sinica.edu.tw) (author/maintainer)<br />
[Wei-Yun Ma](https://www.iis.sinica.edu.tw/pages/ma)@[CKIP](http://ckip.iis.sinica.edu.tw) (maintainer)<br />

## Introduction

This open-source library implements neural CKIP-style Chinese NLP tools.
* (WS) word segmentation
* (POS) part-of-speech tagging
* (NER) named entity recognition

Related demo sites
- [CkipTagger](http://ckip.iis.sinica.edu.tw/service/ckiptagger)
- [CKIP CoreNLP](http://ckip.iis.sinica.edu.tw/service/corenlp)
- [CKIPWS (classic)](http://ckipsvr.iis.sinica.edu.tw)

Features
- Performance improvements
- Do not auto delete/change/add characters
- Support indefinitely long sentences
- Support user-defined recommended-word list and must-word list

ASBC 4.0 Test Split (50,000 sentences)

| Tool | (WS) prec | (WS) rec | (WS) f1 | (POS) acc |
|:-:|:-:|:-:|:-:|:-:|
| CkipTagger       | 97.49% | 97.17% | 97.33% | 94.59% |
| CKIPWS (classic) | 95.85% | 95.96% | 95.91% | 90.62% |
| Jieba-zh_TW      | 90.51% | 89.10% | 89.80% | -- |

## Installation

tl;dr.
```
pip install -U ckiptagger[tf,gdown]
```

CkipTagger is a Python library hosted on PyPI. Requirements:
- python>=3.6
- tensorflow>=1.13.1,<2 / tensorflow-gpu>=1.13.1,<2 (one of them)
- gdown (optional, for downloading model files from google drive)

(Minimum installation) If you have set up tensorflow, and would like to download model files by yourself.
```
pip install -U ckiptagger
```

(Complete installation) If you have just set up a clean virtual environment, and want everything, including GPU support.
```
pip install -U ckiptagger[tfgpu,gdown]
```
