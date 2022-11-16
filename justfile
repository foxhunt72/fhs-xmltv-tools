#!/usr/bin/env just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile test`, for example.


default:
  @just -l

setuptest directory="/tmp/venv":
  #!/usr/bin/env sh
  python -m venv "{{directory}}"
  "{{directory}}/bin/pip3" install -e ".[all]"
  echo "use: source {{directory}}/bin/active to test with python"


setuptest-dev directory="/tmp/venv":
  #!/usr/bin/env sh
  python -m venv "{{directory}}"
  "{{directory}}/bin/pip3" install -e ".[all]"
  "{{directory}}/bin/pip3" install -r requirements-dev.txt
  "{{directory}}/bin/pip3" install -r requirements-flake8.txt
  echo "use: source {{directory}}/bin/active to test with python"

githook-tox:
  #!/usr/bin/env sh
  echo -e "#\!/bin/bash\n\ntox\ntox -e flake8" >.git/hooks/pre-commit
  chmod a+x .git/hooks/pre-commit

githook-commit:
  #!/usr/bin/env sh
  cp .githooks/prepare-commit-msg .git/hooks/

flake8:
  @tox -e flake8

coverage:
  #@tox -e coverage
  "coverage" run --source=src -m pytest tests
  "coverage" report --show-missing
  "coverage" xml -o coverage.xml



# clean some work directories
clean:
  rm -rf .tox

# build python package
build:
  #!/usr/bin/env sh
  export PKG_NAME="$(python setup.py --name)"
  export PKG_VERSION="$(python setup.py --version)"
  export PKG_FILE="dist/${PKG_NAME}-${PKG_VERSION}.tar.gz"
  if ! grep "^- ${PKG_VERSION}:" "CHANGELOG.md"; then
    echo "Missing: - ${PKG_VERSION}: in CHANGELOG.md"
    exit 1
  fi

  # if the package allready exists then just stop
  echo ">>$PKG_FILE<<"
  if test -f "$PKG_FILE"; then
   echo "$PKG_FILE allready exists..."
   exit 1
  fi

  # make sure that everything is pushed to git before building
  if ! git status | grep -q 'working tree clean'; then
    echo "please commit all changes first in git."
    git status
    exit 1
  fi

  echo "checking code using tox before building."
  if ! tox -p; then
    echo "tox error."
    exit 1
  fi

  # build and add git tab
  python setup.py sdist || exit 1
  if ! twine check "$PKG_FILE"; then
    rm "$PKG_FILE"
    exit 1
  fi

  git tag "v${PKG_VERSION}" HEAD && git push -u origin --tags


# publish package to pypi (build first)
publish:
  #!/usr/bin/env sh
  export PKG_NAME="$(python setup.py --name)"
  export PKG_VERSION="$(python setup.py --version)"
  export PKG_FILE="dist/${PKG_NAME}-${PKG_VERSION}.tar.gz"
  twine upload -r pypi "$PKG_FILE" && gh release create "v${PKG_VERSION}" "$PKG_FILE" -F CHANGELOG.md && tweet-fhs-xmltv-tools.sh "$PKG_VERSION"
  # twine upload dist/*

pytest-failure:
  tox -e py310 -- --lf --trace

# bump version number
bumppatch:
  #!/usr/bin/env sh
  bumpversion --allow-dirty --verbose patch
  vi CHANGELOG.md

# edit README.rst
readme:
  #!/usr/bin/env sh
  formiko README.rst

