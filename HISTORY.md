## 0.0.1 (2025-08-29): First release

* Initial commit.
* Added documentation.
* Added `FuzzyNumber`, `FuzzySet`, `TrapezoidalFuzzyNumber`.
* Enabled CI:
  * Test suite.
  * Packaging.
  * Deployment on [readthedoc](https://app.readthedocs.org/)

## 0.0.2 (2025-08-29)

* Documentation:
  * Fixed `installation.md`.
* CI:
  * Fixed `setup.cfg`.

## 0.0.3 (2025-09-02)

* Packaging:
  * Renamed the package to `fuzzy-set-nokia`.
    * The previous name was too close of existing projects already hosted in pypi.org.

## 0.0.4 (2025-09-02)

Packaging:
  * `README.md`: updated links to point to the corresponding page in the [project documentation](https://fuzzy-set.readthedocs.io/).
* CI:
  * `publish_on_pypi.yml`:
    * Fixed [pypi](https://pypi.org/p/fuzzy_set_nokia) and [testpypi](https://test.pypi.org/p/fuzzy_set_nokia) URLs.
    * The `testpypi` workflow no more crash when updating an existing version and displays verbose error messages.
