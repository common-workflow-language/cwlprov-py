# This file is part of cwlprov-py,
# https://github.com/common-workflow-language/cwlprov-py/, and is
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Contact: common-workflow-language@googlegroups.com

# make format to fix most python formatting errors
# make pylint to check Python code for enhanced compliance including naming
#  and documentation
# make coverage-report to check coverage of the python scripts by the tests

MODULE=cwlprov
PACKAGE=cwlprov
EXTRAS=[testing]

# `SHELL=bash` doesn't work for some, so don't use BASH-isms like
# `[[` conditional expressions.
PYSOURCES=$(wildcard ${MODULE}/**.py)
DEVPKGS=diff_cover black pylint pep257 pydocstyle flake8 'tox>4' \
	isort wheel autoflake flake8-bugbear pyupgrade bandit \
	-rmypy-requirements.txt auto-walrus build
COVBASE=coverage run --append

# Updating the Major & Minor version below?
# Don't forget to update pyproject.toml as well
#VERSION=8.2.$(shell date +%Y%m%d%H%M%S --utc --date=`git log --first-parent \
#	--max-count=1 --format=format:%cI`)

## all                    : default task (install cwlprov-py in dev mode)
all: dev

## help                   : print this help message and exit
help: Makefile
	@sed -n 's/^##//p' $<

## cleanup                : shortcut for "make sort_imports format flake8 diff_pydocstyle_report"
cleanup: sort_imports format flake8 diff_pydocstyle_report

## install-dep            : install most of the development dependencies via pip
install-dep: install-dependencies

install-dependencies: FORCE
	pip install --upgrade $(DEVPKGS)
	pip install -r requirements.txt -r mypy-requirements.txt

## install                : install the cwlprov-py package and the cwlprov script
install: FORCE
	pip install .$(EXTRAS)

## dev                    : install the cwlprov-py package in dev mode
dev: install-dep
	pip install -e .$(EXTRAS)

## dist                   : create a module package for distribution
dist: dist/${MODULE}-$(VERSION).tar.gz

dist/${MODULE}-$(VERSION).tar.gz: $(SOURCES)
	python3 -m build

## docs                   : make the docs
docs: FORCE
	cd docs && $(MAKE) html

## clean                  : clean up all temporary / machine-generated files
clean: FORCE
	rm -rf ${MODULE}/__pycache__
	rm -Rf .coverage
	rm -f diff-cover.html

# Linting and code style related targets
## sort_import            : sorting imports using isort: https://github.com/timothycrosley/isort
sort_imports: $(PYSOURCES)
	isort $^

remove_unused_imports: $(PYSOURCES)
	autoflake --in-place --remove-all-unused-imports $^

pep257: pydocstyle
## pydocstyle             : check Python docstring style
pydocstyle: $(PYSOURCES)
	pydocstyle --add-ignore=D100,D101,D102,D103 $^ || true

pydocstyle_report.txt: $(PYSOURCES)
	pydocstyle $^ > $@ 2>&1 || true

## diff_pydocstyle_report : check Python docstring style for changed files only
diff_pydocstyle_report: pydocstyle_report.txt
	diff-quality --compare-branch=main --violations=pydocstyle --fail-under=100 $^

## codespell              : check for common misspellings
codespell:
	codespell -w $(shell git ls-files | grep -v mypy-stubs | grep -v gitignore | grep -v EDAM.owl | grep -v pre.yml | grep -v test_schema)

## format                 : check/fix all code indentation and formatting (runs black)
format: $(PYSOURCES)
	black $^ mypy-stubs

format-check: $(PYSOURCES)
	black --diff --check $^ mypy-stubs

## pylint                 : run static code analysis on Python code
pylint: $(PYSOURCES)
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
                $^ -j0|| true

pylint_report.txt: $(PYSOURCES)
	pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" \
		$^ -j0> $@ || true

diff_pylint_report: pylint_report.txt
	diff-quality --compare-branch=main --violations=pylint pylint_report.txt

.coverage: FORCE
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) validate && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) info && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) who && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) prov && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) inputs && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) outputs && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) runs && ) true
	$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) runtimes && ) true
	#$(foreach RO,$(shell ls test),coverage run -m cwlprov.tool -d test/$(RO) derived && ) true

coverage.xml: .coverage
	coverage xml

coverage.html: htmlcov/index.html

htmlcov/index.html: .coverage
	coverage html
	@echo Test coverage of the Python code is now in htmlcov/index.html

coverage-report: .coverage
	coverage report

diff-cover: coverage.xml
	diff-cover --compare-branch=main $^

diff-cover.html: coverage.xml
	diff-cover --compare-branch=main $^ --html-report $@

## test                   : run the cwlprov-py test suite
test: $(PYSOURCES) FORCE
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) validate && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) info && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) who && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) prov && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) inputs && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) outputs && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) runs && ) true
	$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) runtimes && ) true
	#$(foreach RO,$(shell ls test),python3 -m cwlprov.tool -d test/$(RO) derived && ) true

sloccount.sc: $(PYSOURCES) Makefile
	sloccount --duplicates --wide --details $^ > $@

## sloccount              : count lines of code
sloccount: $(PYSOURCES) Makefile
	sloccount $^

list-author-emails:
	@echo 'name, E-Mail Address'
	@git log --format='%aN,%aE' | sort -u | grep -v 'root'

mypy3: mypy
mypy: $(PYSOURCES)
	MYPYPATH=$$MYPYPATH:mypy-stubs mypy $^

pyupgrade: $(PYSOURCES)
	pyupgrade --exit-zero-even-if-changed --py39-plus $^
	auto-walrus $^

release-test: FORCE
	git diff-index --quiet HEAD -- || ( echo You have uncommitted changes, please commit them and try again; false )
	./release-test.sh

release: release-test
	. testenv2/bin/activate && \
		pip install build && \
		python3 -m build testenv2/src/${PACKAGE} && \
		pip install twine && \
		twine upload testenv2/src/${PACKAGE}/dist/* && \
		git tag ${VERSION} && git push --tags

flake8: $(PYSOURCES)
	flake8 $^

FORCE:

# Use this to print the value of a Makefile variable
# Example `make print-VERSION`
# From https://www.cmcrossroads.com/article/printing-value-makefile-variable
print-%  : ; @echo $* = $($*)
