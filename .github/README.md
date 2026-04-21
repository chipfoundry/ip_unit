# GitHub Actions layout

## Monorepo (`chipfoundry/ip_unit` or equivalent)

Workflows in **this directory** (repository root `.github/workflows/`) are what GitHub runs:

| Workflow | Role |
|----------|------|
| `verify-all.yaml` | Matrix over all `CF_*` IPs; calls `reusable-verify-ip.yml` for each. Triggers on pushes/PRs that touch `CF_*/**` or these workflow files. |
| `reusable-verify-ip.yml` | **Reusable only** — installs Icarus, `cf-ipm`, `verify/pyuvm/requirements.txt`, runs `python test_runner.py` with `SIM=icarus` and `BUSES` from the matrix. |

## Standalone IP repository

If this IP is its **own** Git repo (clone or subtree with the IP at the root), GitHub does **not** read `CF_*/.github/` from a parent monorepo. Copy the IP’s `.github` folder so that `.github/workflows/` sits at the **root** of that repo (same structure as the UART/SPI templates under `CF_UART/.github/`).

Those per-IP `verify.yaml` files assume:

- Repository root = one IP (e.g. `verify/pyuvm` exists at repo root).
- They run **Icarus + Verilator** and optional badge jobs — heavier than the monorepo `verify-all` job.

For parity with CI, standalone workflows should still invoke `python verify/pyuvm/test_runner.py` (or `working-directory: verify/pyuvm` + `test_runner.py`).

## Nested workflow folders (removed)

Workflows must not live under `verify/pyuvm/.github/`; GitHub ignores them.
