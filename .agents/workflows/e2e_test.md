---
description: End-to-End Test
---

# End-to-End (E2E) Test Workflow

This document defines the End-to-End test workflow to verify package distribution and functionality in a clean Docker environment before a production release.

## 1. Overview
The E2E workflow involves verifying the version, running local checks, publishing to TestPyPI, and validating the published package within a Docker container.

## 2. Step-by-Step Workflow

### Step 1: Verify Version Availability
Check if the current version in `src/drawlib/__init__.py` is valid and not already published on TestPyPI.
```bash
./dcli pypi check-version --test-pypi
```

### Step 2: Run Local Quality Checks
Ensure the code passes all linting, type checks, and docstring validations.
```bash
./dcli check all
```

### Step 3: Run Local Unit Tests
Execute the test suite in the local environment.
```bash
./dcli test all
```

### Step 4: Publish to TestPyPI
Upload the package to TestPyPI. This step also updates `pyproject.toml` metadata automatically.
```bash
./dcli pypi publish --test-pypi
```

### Step 5: Ensure Docker is Running
Check the Docker daemon status and start it if it's stopped or in a zombie state (macOS).
```bash
# Check status
./dcli docker daemon-status

# If not running, start it
./dcli docker daemon-start
```

### Step 6: Build Test Docker Image
Build a Docker image that installs the `drawlib` package from TestPyPI. 
```bash
# Example for version 0.2.4.dev3
./dcli docker build-image --version 0.2.4.dev3 --repo test-pypi
```

### Step 7: Run Tests in Docker Container
Verify the published package by running tests inside the newly built Docker container:
```bash
docker run --rm test-drawlib:p3.12_test-pypi_d0.2.4.dev3
```

## 3. Troubleshooting
- **Docker Zombie State**: If Docker is running but not responding, run `./dcli docker daemon-stop` followed by `./dcli docker daemon-start`.
- **Version Conflict**: If `check-version` fails, you may need to increment the version in `src/drawlib/__init__.py`.
- **Docker Build Failure**: Ensure you have a stable internet connection to reach `test.pypi.org`.
