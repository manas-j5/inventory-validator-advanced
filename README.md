# inventory-validator-advanced

Advanced CI practice project for inventory validation with pytest, coverage gates, linting, pull requests, and branch protection.

## CI implementation summary

### Application and tests
- `src/inventory_validator.py` implements:
  - `is_valid_sku(sku)` with strict `INV-` + 4 digits validation and string type checking.
  - `normalize_sku(sku)` returning uppercase for valid values and raising `ValueError("invalid sku")` for invalid SKU format.
  - `stock_status(quantity, reorder_level)` with negative-value rejection and `OUT_OF_STOCK` / `REORDER` / `OK` statuses.
  - `format_item(name, sku, quantity)` with validation and formatted output.
- `tests/test_inventory_validator.py` includes both happy paths and error-path tests.

### Workflows (pull request to `main` only)
- `Tests` (`.github/workflows/tests.yml`): runs complete `pytest` suite.
- `Coverage Check` (`.github/workflows/coverage.yml`):
  - Runs tests with `--cov=src --cov-report=term-missing`.
  - Enforces threshold with `coverage report --include='src/*' --show-missing --fail-under=85`.
- `Lint Check` (`.github/workflows/lint.yml`): runs `pycodestyle` against `src` and `tests`.

### Baseline coverage and gaps (before adding extra tests)
Using only the original four active tests:

```bash
python -m pytest --cov=src --cov-report=term-missing -q \
  tests/test_inventory_validator.py::test_is_valid_sku \
  tests/test_inventory_validator.py::test_is_valid_sku_type_error \
  tests/test_inventory_validator.py::test_stock_status_ok \
  tests/test_inventory_validator.py::test_format_item
```

Observed baseline result:
- Total coverage: **64%**
- Missing lines in `src/inventory_validator.py`: `11-13, 19, 21, 23, 30, 32, 34`
- Function with effectively zero direct test coverage at baseline: `normalize_sku`

After adding branch/error tests, coverage is brought above the required 85% threshold.

### Coverage reporting vs. enforcement
- Reporting only: prints coverage in logs (informational).
- Enforcement: uses `--fail-under=85` so the job exits non-zero when coverage is below threshold.
- This repository uses enforcement in `Coverage Check`, so low coverage blocks merge when required checks are enabled.

### Why `pull_request` is the correct trigger
- The goal is to prevent broken/under-tested code from entering `main`.
- Running checks on PRs provides pre-merge feedback and can be enforced with required status checks.
- A `push`-to-`main` trigger runs too late (after changes are already on the protected branch).

### CI debugging / PR demonstration flow
1. Push feature-branch changes and open PR to `main`.
2. Inspect failed checks in Actions.
3. Open logs and use uncovered lines from coverage output (`term-missing`) to add targeted tests.
4. Re-run CI via new commits until `Tests`, `Coverage Check`, and `Lint Check` pass.

If direct workflow logs are temporarily unavailable in your environment, use these local diagnostics:

```bash
python -m pytest
python -m pytest --cov=src --cov-report=term-missing
python -m coverage report --include='src/*' --show-missing --fail-under=85
pycodestyle --max-line-length=100 src tests
```

Expected failure diagnosis for an under-covered PR: `Coverage Check` fails at the `coverage report --fail-under=85` step and prints missing lines in the job log.

## Branch protection setup (manual)
If branch protection cannot be configured from this automation environment, configure it in GitHub UI:

1. Open repository **Settings → Branches → Add branch protection rule**.
2. Branch name pattern: `main`.
3. Enable **Require a pull request before merging**.
4. Enable **Require status checks to pass before merging**.
5. Select required checks:
   - `Coverage Check`
   - `Lint Check`
6. Save rule.

Equivalent API flow (requires admin token with repo permissions):
- Endpoint: `PUT /repos/{owner}/{repo}/branches/main/protection`
- Include required status checks and pull-request review requirements in payload.
