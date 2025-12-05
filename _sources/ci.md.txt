# CI

This page gather the steps to set up the Continuous Integration by reusing
the files related to another similar project. The relevant files are:

* `pyproject.toml`: Project settings
* `.github/workflows/*.yml`: GitHub actions
* `.readthedocs.yml`: Readthedoc workflow

## Build

If the project is build using `poetry`, ensure this is reflected in `.github/workflows/build.yml`.

## PyPI 

1. In `.github/workflows/publish_on_pypi.yml`:

* update the PyPI URL of the project
* enable/remove in the `with:` statement:
  * `verbose: true`
  * `skip-existing: true`

2. Configure the project [Test PyPI](https://test.pypi.org/).

  * Connect to your [Test PyPI](https://test.pypi.org/) account.
  * [Add a new pending publisher](https://test.pypi.org/manage/account/publishing/). This allows GitHub to push stuff to [Test PyPI](https://test.pypi.org/) without configuring any token.
    * __Name of the PyPI project:__ name of the PyPI package (defined in `poetry.toml`, e.g., `fuzzy-set-nokia`)
    * __Owner:__ 2nd part in the GitHub URL repository (e.g., `Nokia-Bell-Labs` in [https://github.com/Nokia-Bell-Labs/fuzzy-set](https://github.com/Nokia-Bell-Labs/fuzzy-set)).
    * __Repository name:__ 3rd part in the GitHub URL repository (e.g., `fuzzy-set` in [https://github.com/Nokia-Bell-Labs/fuzzy-set](https://github.com/Nokia-Bell-Labs/fuzzy-set)).
    * __Workflow name:__ Filename of publishing workflow (e.g., `publish_on_pypi.yml` in [https://github.com/Nokia-Bell-Labs/fuzzy-set/blob/main/.github/workflows/publish_on_pypi.yml](https://github.com/Nokia-Bell-Labs/fuzzy-set/blob/main/.github/workflows/publish_on_pypi.yml)).
    * __Environment name:__ `testpypi` (reported in GitHub environments)

3. Repeat the previous steps for [PyPI](https://pypi.org/).

4. Push an update using `git push` and a tag using `git push --tags`. As stated in `.github/workflows/publish_on_pypi.yml` this respectively updates [Test PyPI](https://test.pypi.org/) and [PyPI](https://pypi.org/)

5. Update the related badge in `README.md`. Test the link and image URLs of the badge are correct with a web browser.

## ReadTheDoc

1. If the project is build using `poetry`, ensure this is reflected in `.readthedocs.yml`. In particular, ensure that the dependencies needed to build the documentation will be deployed.

2. Connect to your [Readthedoc](https://app.readthedocs.org/dashboard/) account.
3. Create a new project. This name is used by your dashboard. You should choose the name of the PyPI package but it's not mandatory. If the repository is not found automatically, [configure it manually](https://app.readthedocs.org/dashboard/import/manual/):

  * __Name:__ this name is used to craft the URL that will serve the documentation.
  * __Repository URL:__ the GitHub URL (e.g., [https://github.com/Nokia-Bell-Labs/fuzzy-set](https://github.com/Nokia-Bell-Labs/fuzzy-set)).
  * __Default branch:__ usually `main`. Old repositories might use `master`.
  * __Language__ English

4. If readthedoc displays _Unable to attach webhook to this project Could not add webhook for "fuzzy-set". Make sure [you have the correct GitHub permissions](https://docs.readthedocs.io/page/webhooks.html)._:

  * If this is a repository attached to an organization, browse your Github profile _> Application > Authorized OAuth Apps > Read the Docs Community (readthedocs.org) > Organization access_. Select the appropriate organization and request an access if not yet granted.
  * In [the Integration settings of your Readthedoc project](https://app.readthedocs.org/dashboard/fuzzy-set/integrations/), try to resync the hook.
  * If it fails, try [configure the webhook manually](https://docs.readthedocs.com/platform/stable/guides/setup/git-repo-manual.html)
