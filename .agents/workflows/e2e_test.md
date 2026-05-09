---
description: End-to-End Test
---

# End-to-End (E2E) Test Workflow

This document defines the End-to-End test workflow to verify the package distribution and its functionality in a clean Docker environment before a production release.

## 1. Overview
The E2E workflow involves verifying the version, running local checks, publishing to TestPyPI, and validating the published package within a Docker container.

## 2. Step-by-Step Workflow

### Step 1: Verify Version Availability
Check if the current version in `pyproject.toml` is valid and not already published on TestPyPI.
```bash
task pypi_test:check-new-version
```

### Step 2: Run Local Quality Checks
Ensure the code passes all linting and type checks.
```bash
task check
```

### Step 3: Run Local Unit Tests
Execute the unit tests for the current version (e.g., v0.2) in the local environment.
```bash
task utest:v0.2:all
```

### Step 4: Publish to TestPyPI
Upload the package to TestPyPI. This step also updates the version in `pyproject.toml` if necessary and checks the version again.
```bash
task pypi_test:publish
```

### Step 5: Ensure Docker is Running
Check the Docker daemon status and start it if it's stopped or in a zombie state (macOS).
```bash
# Check status
task docker:daemon:status

# If not running or zombie, start it
task docker:daemon:start
```

### Step 6: Build Test Docker Image
Build a Docker image that installs the `drawlib` package from TestPyPI. 
You must specify the `VERSION` (found in `pyproject.toml`) and `REPO=test-pypi`.
```bash
# Example for version 0.2.4.dev3
task docker:test-images:build VERSION=0.2.4.dev3 REPO=test-pypi
```

### Step 7: Run Unit Tests in Docker
Verify the published package by running the unit tests inside the newly built Docker container.
The `IMAGE` tag follows the pattern: `test-drawlib:p<PYTHON>_<REPO>_d<VERSION>`.
```bash
# Example for Python 3.12, TestPyPI, and version 0.2.4.dev3
task utest:docker IMAGE=test-drawlib:p3.12_test-pypi_d0.2.4.dev3
```

## 3. Troubleshooting
- **Docker Zombie State**: If Docker is running but not responding, run `task docker:daemon:stop` followed by `task docker:daemon:start`.
- **Version Conflict**: If `check-new-version` fails, you may need to increment the version in `pyproject.toml`.
- **Docker Build Failure**: Ensure you have a stable internet connection to reach `test.pypi.org`.
