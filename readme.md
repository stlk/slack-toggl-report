# Slack toggl report

This tool uses the [Toggl Reports API](https://github.com/toggl/toggl_api_docs/blob/master/reports.md) to generate a status report that is broken down by User -> Client -> Project -> Tasks.

It currently spits out the report in markdown to stdout.

```
usage: dotenv-run python run-report.py [-h] start end

positional arguments:
  start       The start date in YYYY-MM-DD format
  end         The end date in YYYY-MM-DD format

optional arguments:
  -h, --help  show this help message and exit
```

## Installation

Python 3.5 or newer is required. This project uses [pipenv](https://docs.pipenv.org/). You can install it using `pip install pipenv`.

```
pipenv install
```

## Usage

You can use `pipenv run python slack-report.py` to post report to slack.

## Contributors

Based on work of James S. Martin https://github.com/jsmartin/toggl_report
