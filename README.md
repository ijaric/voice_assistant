# Python Contrib

Python packages mono-repository

## Development

### Global dependencies

- node
- poetry

### Makefile commands

#### Root commands

- `make init` - Initialize repository
- `make lint` - Lint repository
- `make lint-fix` - Auto-fix repository
- `make test` - Test repository
- `make clean` - Clean up repository
- `make all-init` - Init all packages
- `make all-lint` - Lint all packages
- `make all-lint-fix` - Auto-fix all packages
- `make all-test` - Test all packages
- `make all-clean` - Clean all packages
- `make all-dependencies-update` - Update dependencies in all packages
- `make ci-init` - CI-specific version of init command

#### Common package commands

- `make init` - Initialize package
- `make lint` - Lint package
- `make lint-fix` - Auto-fix package
- `make test` - Test package
- `make clean` - Clean up package folder
- `make dependencies-update` - Update not restricted dependencies
- `PYPI_WRITER_PASSWORD=... make ci-login-pypi-publish` - Login to personal pypi with publish rights
- `make ci-test` - Test package in CI
- `make ci-package-build` - Builds package in CI
- `make ci-package-publish` - Publishes package in CI
