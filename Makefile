SHELL := /bin/bash

doc:
	ansible-doc-extractor docs/source/modules plugins/modules/*.py
	sphinx-build -b html docs/source docs/build
	touch docs/build/.nojekyll
