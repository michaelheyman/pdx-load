# pdx-load

[pdx-load](https://github.com/michaelheyman/pdx-load/) is part of the
[pdx-schedule](https://github.com/michaelheyman/pdx-schedule/) project.

Runs a Cloud Function that retrieves the latest processed structured JSON data
from a bucket that has the output of running
[pdx-transform](https://github.com/michaelheyman/pdx-transform/).

The purpose of this Cloud Function is then to load the schedule data into Cloud
Datastore.

## Setup

### Create Virtual Environment

```bash
pyenv virtualenv 3.7.3 pdx-load-3.7.3
pyenv activate pdx-load-3.7.3
```

### Install Requirements

```bash
pip -r install requirements.txt
```

### Install Git Hooks

See [.pre-commit-config.yaml](.pre-commit-config.yaml) for information on which hooks are configured.

```bash
pre-commit install
```

```bash
pre-commit install -t pre-push
```

## Running

Run the application by executing

```bash
python -m app
```

## Testing

Ensure that `pytest` and `pytest-cov` are installed:

```bash
pip install pytest pytest-cov
```

Run `pytest` with verbose output:

```bash
pytest -vv
```

Run `pytest` with coverage:

```bash
pytest --cov=app tests/
```

```bash
pytest --cov-report html --cov=app tests/
```

## Deploying Cloud Function

Run the `deploy` script at the root of the project to deploy the Cloud Function.

There is the potential to reduce the memory requirements of the Function.
