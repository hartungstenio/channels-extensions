# Project Guidelines

## Project Structure

- Application code lives in `src/channels_extensions/`.
- Tests live in `tests/` and use the Django project in `testproj/`.
- This is a set of small, independent extensions for Django Channels (channel layers, consumers, ASGI middlewares); keep each module self-contained.
- ASGI middlewares must work for both `http` and `websocket` scopes unless documented otherwise.

## Development Commands

- Run the full test matrix with `hatch test`.
- Run focused tests with `hatch run pytest tests/<test_file>.py`.
- Run code quality checks with `hatch check code`.
- Verify formatting with `hatch check fmt`.
- Run type checks with `hatch run mypy src tests`.

## Python and Django Conventions

- Support the Python, Django and Channels versions declared in `pyproject.toml`.
- Preserve strict typing and existing type annotations; the code is checked with mypy (with `django-stubs` and `types-channels`).
- Follow the existing Ruff configuration, including a 120-character line limit.
- Use `asyncio_extensions.TaskGroup` instead of `asyncio.TaskGroup` (enforced by Ruff).
- Use Django and Channels APIs (`channels.db`, `channels.middleware.BaseMiddleware`, `asgiref.sync`) rather than reimplementing them.
- Keep sync and async variants of a paired API behaviorally equivalent.

## Testing Expectations

- Add or update focused tests for every behavior change.
- Include both synchronous and asynchronous coverage when changing a paired API.
- Run the focused test file first, then the full suite before finishing.
- Group tests for a class or module in a single `Test<Name>` class and prefix each test with `test_<method>_` where it applies.
- Order test classes and methods to match the definition order in the corresponding source file.
- Tests that touch the database need `pytest.mark.django_db`; use mocks for ASGI `receive`/`send`/`inner`.

## GitHub Actions

- Every action used in `.github/workflows/` (and local `action.yml` files) is pinned by `.github/workflows/actions.lock`, managed by the `gh actions-lock` extension.
- After editing a workflow or `action.yml`, run `gh actions-lock` and commit the lockfile in the same change. Never edit `actions.lock` by hand.
- Check with `gh actions-lock --verify` (read-only). If a tag moved upstream, investigate before running `gh actions-lock --relock`; never use `--accept-moved` without confirming why the commit disappeared.
- New workflows must declare minimal `permissions` and use `persist-credentials: false` on `actions/checkout`.

## Change Scope

- Keep changes minimal and consistent with neighboring code.
- Do not modify unrelated user changes.
- Use Conventional Commits for commit messages, such as `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.
- Update `README.md` when a change affects documented behavior, public APIs, configuration, installation, or usage.
- Update `CHANGELOG.md` (under `[UNRELEASED]`) for user-visible changes that are not yet part of a published release.
