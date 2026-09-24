# service-template

A GitHub template for spec-first Python services: OpenAPI 3 contract in, a
hexagonal-architecture Connexion 3 (ASGI) service out — with the code generator
vendored into the repo so you never leave your service to regenerate.

```
HTTP -> Connexion -> generated handler -> request adapter -> port -> service -> domain
                     (validates DTOs,     (DTO <-> domain)   (Protocol) (yours)
                      picks status)
```

Everything runs in Docker (app + Postgres via compose, plain `pip` inside the
image). No local Python, virtualenv or package manager needed.

## Create a service

1. **Use this template** on GitHub (or clone and re-init), then clone your new repo.
2. Replace `openapi/openapi.yml` with your contract. Every operation needs an
   `operationId` and a tag; bodies should `$ref` schemas under `components/schemas`.
3. One-time scaffold, then run:

   ```sh
   ./dev.sh init        # writes app/, tests/, README.md from the spec
   ./dev.sh up          # postgres + app with hot reload on :8080
   ```

   Swagger UI is at `http://localhost:8080/<base-path>/ui` (`./dev.sh docs` opens it).
   Every endpoint answers `501 Not Implemented` until you fill in the matching
   method in `app/application/services/<tag>_service.py`.
4. Commit. The generated `README.md` documents the service layout and day-to-day
   workflow (`./dev.sh help` lists every command). Copy `.env.example` to `.env`
   to change host ports or log level.

The example `openapi/openapi.yml` shipped here is a small Widget service so the
template runs out of the box; `./dev.sh init` on a fresh checkout is a working demo.

## Evolve a service

Edit `openapi/openapi.yml`, then:

```sh
./dev.sh sync
```

`sync` rewrites `app/generated/` (Pydantic models + handlers) and creates
adapter/port/service stubs for any new tag. It never touches files you own; if a
new tag appeared it tells you to wire the adapter into `app/main.py`.

## Ownership

| Path | Owner | On `sync` | On `upgrade` |
| --- | --- | --- | --- |
| `app/generated/**` | generator | overwritten | overwritten (via sync) |
| `app/adapters/inbound/*_adapter.py`, `app/application/ports/*`, `app/application/services/*` | you (scaffolded once) | created if missing | untouched |
| `app/main.py`, `app/settings.py`, `app/domain/**`, `app/adapters/outbound/**`, `tests/**`, `README.md` | you (written by `init`) | untouched | untouched |
| `Dockerfile`, `compose.yaml`, `requirements*.txt`, `pyproject.toml`, `alembic.ini`, `migrations/` | you (shipped plain) | untouched | untouched |
| `dev.sh`, `scripts/`, `tools/service_gen/`, `.github/workflows/ci.yml` | template | untouched | **replaced** |

## CI

Every service gets `.github/workflows/ci.yml` out of the box. On pushes to `main`
and on pull requests it runs `./dev.sh build && ./dev.sh check` — the same dev
image and commands as locally — and builds the production image once `app/`
exists. `check` is, in order:

| Step | Fails when |
| --- | --- |
| `check-generated` | `app/generated/` doesn't match what `sync` produces from the spec |
| `lint` | ruff check / format, or `openapi/openapi.yml` is not valid OpenAPI 3 |
| `typecheck` | mypy `--strict` |
| `test` | pytest (against the compose Postgres) |
| `check-migrations` | `alembic upgrade head` fails, or ORM models drifted from the migrations |

It is template-owned, so put service-specific jobs (deploy, publish) in
separate workflow files.

## Upgrading a service to a newer template

```sh
./dev.sh upgrade            # latest main
./dev.sh upgrade v0.3.0     # a tag or branch
```

Replaces the template-owned paths from this repo, records the version in
`TEMPLATE_VERSION`, rebuilds the dev image and runs `sync`. Review the result as
one PR: generator diff + regenerated code + any manual edits the release notes ask
for. Set `TEMPLATE_REPO` to point at a fork or local clone.

## Layout of this repo (= an un-initialised service)

```
openapi/openapi.yml      example contract; a service replaces this
Dockerfile               dev target (tooling, bind mount) and prod target (slim)
compose.yaml             app + postgres:16 (.env.example lists the knobs)
requirements.txt         runtime deps        requirements-dev.txt  tooling + generator deps
pyproject.toml           ruff / mypy / pytest config only
alembic.ini, migrations/ async Alembic wired to app.settings
dev.sh                   dispatcher: ./dev.sh <cmd> -> scripts/<cmd>.sh
scripts/                 one command per file; line 2 is its help text
tools/service_gen/       the generator: cli.py, spec.py, render.py, templates/, tests/
.github/workflows/ci.yml lint + typecheck + test in Docker; prod image build
TEMPLATE_VERSION         what a service was last upgraded to
```

The service package is always `app/` and settings use the `APP_` env prefix, so
Dockerfile, compose and Alembic are plain files rather than templates.

## Developing the template

```sh
./dev.sh test tools/service_gen/tests    # generator tests (init + sync + a full request flow)
./dev.sh lint && ./dev.sh typecheck
./dev.sh init && ./dev.sh up             # try the result; `git clean -fd app tests && git checkout README.md` to reset
```

Templates live in `tools/service_gen/templates/`: `project/` is written once by
`init`, `generated/` is rewritten by every `sync`, `stubs/` are created only when
missing. When you tag a release, update `TEMPLATE_VERSION` and note any manual
steps services need in the release notes.
