SHELL := /bin/bash

doc:
	ansible-doc-extractor docs/source/modules plugins/modules/*.py
	sphinx-build -b html docs/source docs
	touch docs/.nojekyll
