# Please do not use this library

This is a fork of [Uniplot]() and attempts to see if my CI/CD can replace the approach taken by [Uniplot](). I do not pretent this mine and it is merely an experiment.


## Lessions learnt

### Setup.py and Setup.cfg work together

Alongside `pipenv` they automatically create and destroy the `pyproject.toml`.
In addition, I could set `extra_dependencies` in `setup.cfg` and they need to remain in `setup.py` inorder for `pip -e .[dev]` to install development dependencies.

### Version release process

- Given you have just published `v0.0.1`, create a `H3` heading in `CHANGELOG.md` for `v0.0.2`.  
- Commit away!
- When ready to announce a version bump, with all modified files commited, run `make patch` to bump version and create a draft release note.  ⚠️ At this point further commits won't be part of this release.
- publish the draft release with changelogs when ready.
- All commits from the version patch will belong to the next version bump.

### How to reset a library version

make sure `.bumpversion.cfg` and `setup.py` have their versions set to `0.0.0`

### To Manually Publish do the following

Ensure make build-check is run
Then run make publish

I have adjusted `Makefile` to run `build-check` before running `publish`.

### Library folder name must match the module name

This ensures `__init__.py` belong to the module name not `src`.

### On setting up CI/CD

You must depoy version `0.0.0` manually, that will create a project instance on PyPi. Create a token against that project and add it as a GitHub Actions Secret under the key `PYPI_API_TOKEN`.

### On Testing

`tox` command for tests must be following or the incorrect file will be targetted. [SO-Link](https://stackoverflow.com/a/49488748). Uniplot author interesting does the same thing!
```
python -m pytest
```