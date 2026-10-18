# tax_service

A jurisdiction-agnostic personal income tax computation service. Canada is the pilot,
with Ontario as the first jurisdiction. The engine composes tested, typed capabilities
according to a per-jurisdiction manifest, with rates and thresholds held as versioned
data. Every result can be reproduced and explained line by line.

**Status:** early development. The engine design is in [`design.md`](design.md) and is
still a draft. The HTTP API is not designed yet. `openapi/openapi.yml` still holds the template's example
Widgets endpoints, which will be replaced.

## Conventions

These apply to everyone working on the repo, people and coding agents alike.

- **Design source.** `design.md` is the reference for the tax engine.
- **Test-driven development.** Write a failing unit test first, run it and watch it
  fail, then write the code that makes it pass.
- **Unit tests are required** for all code.
- **The tax engine lives in `app/domain/`.** Its behavior belongs on the domain objects
  themselves. Application services stay thin: they load data and hand it to the domain.
- **Real jurisdiction names stay in their jurisdiction's package.** Real names and data
  appear only in `app/jurisdictions/<x>/` and `tests/jurisdictions/<x>/`. Generic code and
  tests use made-up names and values.
- **Adapter direction means who starts the call**, not which way data flows.
  `adapters/inbound/` holds driving adapters, which call the application.
  `adapters/outbound/` holds driven adapters, which the application calls, including
  ones that only read data.

## Architecture

The service is hexagonal and spec-first, built on Connexion 3 (ASGI). A request flows
`Connexion -> generated handler -> inbound adapter -> port -> service -> domain`.

```
openapi/openapi.yml       the HTTP contract; edit this first
app/
  main.py                 composition root: the only place that wires concrete classes
  settings.py             configuration from APP_* environment variables
  domain/                 the tax engine: entities, value objects, errors
  application/
    ports/                Protocols the adapters call or implement
    services/             thin orchestration over the domain
  adapters/
    inbound/              HTTP request adapters (DTO -> domain -> DTO), trace renderers
    outbound/             driven adapters: database, files
  jurisdictions/          one package per jurisdiction: catalog, manifests, parameter data
  registrations.py        explicit lists of core packages and jurisdiction packages
  generated/              written by the generator from the spec; never edit
migrations/               Alembic (async)
tests/
design.md                 tax engine design
```

### Adding a jurisdiction

Copy `app/jurisdictions/ca_on/` to `app/jurisdictions/<x>/`, named from the jurisdiction
code (`CA-QC` -> `ca_qc`), and change:

- `__init__.py`: `NAMESPACE = "<code lower-cased>"`, e.g. `"ca-qc"`.
- `catalog.py`: `CATALOG`, an `ArtifactCatalog` for that namespace declaring the jurisdiction's
  artifact kinds, with `non_negative=True` on every money kind the return cannot make negative.
  Declaring only records a kind; importing the package registers nothing.
- `manifests/`: the manifest(s) selecting capabilities and filling their slots: parameter
  slots with parameter families, artifact slots with artifact identifiers (a consumed list slot
  takes a YAML list of them, in order). Each manifest also requires `inputs:` and `outputs:`,
  the artifact identifiers a computation starts from and returns.
- `parameters/`: one dataset per family and tax year, at `parameters/<family>/<year>.yaml`
  for family `<namespace>/<family>`.

Then list it in `app/registrations.py`: import `app.jurisdictions.<x>` and add it to
`JURISDICTIONS`. Catalogs register at startup: the composition root calls
`JURISDICTIONS.register()`, which imports each listed package's `catalog` module and registers its
`CATALOG` in the shared artifact registry. Its tests go under `tests/jurisdictions/<x>/`.

Raise `DomainError` subclasses from `app/domain/errors.py` for business failures.
`main.py` maps them to RFC 7807 problem responses.

## Development

Everything runs in Docker through `./dev.sh`, so no local Python is needed.

```sh
./dev.sh up            # app on http://localhost:8080/api/v1/ui, postgres on :5432
./dev.sh test          # pytest
./dev.sh check         # what CI runs: generated-code drift, lint, mypy, pytest, migrations
./dev.sh fmt           # ruff format and autofix
./dev.sh shell         # bash inside the app container
./dev.sh psql          # psql into the dev database
./dev.sh fresh         # wipe the database volume and start over
./dev.sh help          # every command
```

`./dev.sh up` hot-reloads on source changes. Runtime dependencies are in
`requirements.txt` and tooling in `requirements-dev.txt`; run `./dev.sh build` after
changing either. Settings come from the environment with the `APP_` prefix. Copy
`.env.example` to `.env` to change host ports or the log level.

### Endpoints

1. Edit `openapi/openapi.yml`. Every operation needs an `operationId` and a tag.
2. Run `./dev.sh sync`. It regenerates `app/generated/` and creates stubs for new tags
   and operations, without touching files that already exist.
3. For a new tag, add its adapter to `build_adapters()` in `app/main.py`.
4. Implement the service method. Unimplemented ones answer HTTP 501.

### Persistence

1. Add an ORM model subclassing `Base` under `app/adapters/outbound/db/` and import it
   in that package's `__init__.py` so Alembic sees it.
2. Run `./dev.sh revision "describe the change"`, then `./dev.sh migrate`.
3. Write a repository that takes the session factory, put an outbound port in front of
   it, and pass it to the service in `build_adapters()`.

### Health checks

`/status/livez` always answers ok. `/status/readyz` runs every `ReadinessProbe` passed
in `build_adapters()` and answers 503 on the first failure. The database probe is wired
by default. Add one probe per external dependency.

## Service template

This repo was created from
[service-template](https://github.com/The-Pied-Piper/service-template). The template
owns `dev.sh`, `scripts/`, `tools/service_gen/` and `.github/workflows/ci.yml`. Don't
edit those here; change them in the template and pull the update:

```sh
./dev.sh upgrade            # latest main
./dev.sh upgrade v0.2.0     # a tag or branch
```

The upgrade replaces those paths, records the version in `TEMPLATE_VERSION` and runs
`sync`. Review the result as one pull request. Everything else, this README included,
belongs to this project.
