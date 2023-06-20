SHELL := /bin/bash

collection:
	ansible-galaxy collection build

doc:
	ansible-doc-extractor docs/source/modules plugins/modules/*.py
	sphinx-build -b html docs/source docs
	touch docs/.nojekyll
