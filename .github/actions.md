## 1. Events (`on`)

Events determine **when** a workflow starts.

### Common Events

```yaml
on: push
```

```yaml
on: pull_request
```

```yaml
on: workflow_dispatch
```

```yaml
on: schedule
```

### Frequently Used Events

| Event | Description |
|--------|-------------|
| `push` | Trigger on every push |
| `pull_request` | Trigger on PR creation or update |
| `workflow_dispatch` | Manually trigger a workflow from GitHub UI |
| `schedule` | Trigger using a cron expression |
| `release` | Trigger when a release is published |
| `issues` | Trigger on issue events |
| `issue_comment` | Trigger on issue or PR comments |
| `workflow_call` | Invoke a reusable workflow |

---

## 2. Expressions (`${{ }}`)

Expressions are evaluated inside the `${{ }}` syntax.

### Examples

```yaml
${{ github.actor }}
${{ github.repository }}
${{ github.ref }}
${{ github.sha }}
${{ env.PYTHON_VERSION }}
${{ secrets.JWT_SECRET }}
```

### Common Uses

- Conditional execution
- Accessing variables
- Reading secrets
- Matrix values
- Workflow metadata

---

## 3. Contexts

Contexts expose metadata about the workflow, repository, runner, and execution.

| Context | Description |
|---------|-------------|
| `github` | Repository and workflow information |
| `env` | Environment variables |
| `runner` | Runner details |
| `job` | Current job information |
| `steps` | Outputs from previous steps |
| `matrix` | Matrix strategy values |
| `needs` | Outputs from dependent jobs |
| `vars` | Repository/Organization variables |
| `secrets` | Repository secrets |
| `inputs` | Inputs to reusable workflows |

Example:

```yaml
${{ github.actor }}
```

Returns the username that triggered the workflow.

---

## 4. Default Working Directory

By default, all commands execute from the repository root.

Change the working directory:

```yaml
defaults:
  run:
    working-directory: backend
```

---

## 5. Shell

Specify which shell executes the commands.

```yaml
run: echo "Hello"
shell: bash
```

Supported shells:

- `bash`
- `sh`
- `PowerShell`
- `cmd`

---

## 6. Step Outputs

A step can expose values for later steps.

```yaml
- id: version
  run: echo "VERSION=1.0" >> $GITHUB_OUTPUT
```

Access the output:

```yaml
${{ steps.version.outputs.VERSION }}
```

---

## 7. Job Outputs

Jobs can expose outputs to dependent jobs.

```yaml
outputs:
  image: ${{ steps.build.outputs.image }}
```

Use in another job:

```yaml
${{ needs.build.outputs.image }}
```

---

## 8. Job Dependencies (`needs`)

Define execution order between jobs.

```yaml
deploy:
  needs:
    - build
    - test
```

The `deploy` job starts only after both jobs complete successfully.

---

## 9. `continue-on-error`

Allow a step to fail without failing the entire workflow.

```yaml
continue-on-error: true
```

Useful for:

- Experimental tests
- Optional linting
- Non-blocking checks

---

## 10. Timeout

Prevent workflows from running indefinitely.

```yaml
timeout-minutes: 20
```

Can be configured for both jobs and steps.

---

## 11. Permissions

Restrict permissions of the automatically generated `GITHUB_TOKEN`.

```yaml
permissions:
  contents: read
```

Example:

```yaml
permissions:
  contents: read
  packages: write
```

> **Best Practice:** Always follow the **Principle of Least Privilege**.

---

## 12. Concurrency

Prevent duplicate workflow executions.

```yaml
concurrency:
  group: production
  cancel-in-progress: true
```

Commonly used in deployment pipelines.

---

## 13. Reusable Workflows

Create workflows that can be shared across repositories.

Reusable workflow:

```yaml
on:
  workflow_call:
```

Invoke it:

```yaml
uses: org/repo/.github/workflows/build.yml@main
```

---

## 14. Composite Actions

Bundle multiple steps into a reusable custom action.

Project structure:

```text
.github/
└── actions/
    └── setup-python/
        └── action.yml
```

Useful for reducing duplicated workflow logic.

---

## 15. Self-hosted Runners

Run workflows on your own infrastructure.

```yaml
runs-on: self-hosted
```

### Advantages

- Faster builds
- Private infrastructure
- Custom software
- GPU support

---

## 16. Environments

Protect deployment targets.

```yaml
environment:
  name: production
```

Features:

- Required approvals
- Environment secrets
- Deployment history
- Protection rules

---

## 17. Services

Run supporting containers alongside your job.

```yaml
services:
  postgres:
    image: postgres:16
```

Common services:

- PostgreSQL
- MySQL
- Redis
- MongoDB

---

## 18. Containers

Execute an entire job inside a Docker container.

```yaml
container:
  image: python:3.12
```

Provides a consistent runtime environment.

---

## 19. Cron Scheduling

Automatically execute workflows on a schedule.

```yaml
on:
  schedule:
    - cron: "0 0 * * *"
```

Runs every day at **00:00 UTC**.

Typical use cases:

- Nightly builds
- Backups
- Health checks
- Dependency updates

---

## 20. Artifacts vs Cache

| Cache | Artifacts |
|--------|-----------|
| Speeds up future workflow runs | Stores generated files |
| Automatically restored | Downloaded manually or by later jobs |
| Used for dependencies | Used for reports, binaries, logs |
| Temporary optimization | Persistent workflow output |

---

## 21. Variables vs Secrets

| Variables | Secrets |
|-----------|---------|
| Plain text | Encrypted |
| Visible in logs | Masked in logs |
| Configuration values | Passwords, API keys, Tokens |

Examples:

```yaml
${{ vars.APP_NAME }}
```

```yaml
${{ secrets.DOCKER_TOKEN }}
```

---

## 22. GitHub-hosted Runner Lifecycle

Every workflow gets a **fresh virtual machine**.

```text
Runner Starts
      │
      ▼
Checkout Code
      │
      ▼
Execute Steps
      │
      ▼
Upload Artifacts
      │
      ▼
Runner Destroyed
```

Only **Artifacts** and **Cache** persist after the runner is destroyed.

---

## 23. Common Built-in Variables

| Variable | Description |
|----------|-------------|
| `github.actor` | User who triggered the workflow |
| `github.ref` | Current branch or tag |
| `github.sha` | Commit SHA |
| `github.repository` | Repository name |
| `runner.os` | Runner operating system |
| `runner.arch` | Runner architecture |

---

## 24. Matrix Builds

Instead of writing multiple jobs for different environments, use a **Matrix Strategy**.

Example:

```yaml
strategy:
  matrix:
    python-version:
      - "3.10"
      - "3.11"
      - "3.12"
```

Usage:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: ${{ matrix.python-version }}
```

GitHub automatically creates **parallel jobs** for every matrix combination.

---

## 25. Uploading Artifacts

Store workflow outputs for later download.

Upload artifacts:

```yaml
- name: Upload Test Report
  uses: actions/upload-artifact@v4
  with:
    name: test-report
    path: reports/
```

Upload only on failure:

```yaml
- name: Upload Test Report
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: test-report
    path: reports/
```
