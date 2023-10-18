SHELL := /bin/bash

collection: clean test
	ansible-galaxy collection build

test:
	ansible-test sanity
	ansible-lint

doc:
	ln -f CHANGELOG.rst docs/source/CHANGELOG.rst
	ln -f roles/cluster_prepare/README.md docs/source/roles/cluster_prepare.md
	ln -f roles/cluster_create/README.md docs/source/roles/cluster_create.md
	ansible-doc-extractor docs/source/modules plugins/modules/*.py
	sphinx-build -b html docs/source docs
	touch docs/.nojekyll

clean:
	rm -rf docs/*.html docs/*.js docs/source/CHANGELOG.rst docs/source/modules/*.rst docs/source/roles/*.md docs/objects.inv docs/modules docs/roles docs/_static docs/_sources docs/.doctrees docs/.buildinfo plugins/modules/__pycache__ cache tests *.tar.gz *.swp
