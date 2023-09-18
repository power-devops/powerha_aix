SHELL := /bin/bash

collection:
	ansible-galaxy collection build

test:
	ansible-test sanity

doc:
	ln CHANGELOG.rst docs/source/CHANGELOG.rst
	ansible-doc-extractor docs/source/modules plugins/modules/*.py
	sphinx-build -b html docs/source docs
	touch docs/.nojekyll
