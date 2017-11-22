# Slack toggl report

This tool uses the [Toggl Reports API](https://github.com/toggl/toggl_api_docs/blob/master/reports.md) to generate a status report that is broken down by User->Client->Project->Tasks.

It currently spits out the report in markdown to stdout.

```
usage: dotenv-run python run-report.py [-h] start end

positional arguments:
  start       The start date in YYYY-MM-DD format
  end         The end date in YYYY-MM-DD format

optional arguments:
  -h, --help  show this help message and exit
```

## Slack

You can use `dotenv-run python slack-report.py` to post report to slack.

## Requirements

Python 3.5

```
pip install -r requirements.txt
```

## Contributors

Based on work of James S. Martin https://github.com/jsmartin/toggl_report
