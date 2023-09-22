SHELL := /bin/bash

collection: clean test
	ansible-galaxy collection build

test:
	ansible-test sanity
	ansible-lint

doc:
	ln -f CHANGELOG.rst docs/source/CHANGELOG.rst
	ansible-doc-extractor docs/source/modules plugins/modules/*.py
	sphinx-build -b html docs/source docs
	touch docs/.nojekyll

clean:
	rm -rf docs/*.html docs/*.js docs/source/CHANGELOG.rst docs/source/modules/*.rst docs/objects.inv docs/modules docs/_static docs/_sources docs/.doctrees docs/.buildinfo plugins/modules/__pycache__ cache tests *.tar.gz *.swp
