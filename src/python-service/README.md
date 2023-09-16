# Python Service Example Backend

Python Service Example Backend

## Development

### Global dependencies

- poetry

### Makefile commands

- `make init` - Initialize service
- `make lint` - Lint service
- `make lint-fix` - Auto-fix service
- `make test` - Test service
- `make clean` - Clean up service
- `make dev-server-start` - Start dev server
- `make test-coverage-run` - Collect test coverage data
- `make test-coverage-report` - Show coverage report in console
- `make test-coverage-html` - Prepare and show coverage report in browser
- `make ci-image-build` - Build production container
- `make ci-image-push` - Push production container to yccr

### Environment variables

- `APP_ENV` - Application environment (development, production, etc.)
- `APP_VERSION` - Application version
