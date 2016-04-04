hug_sentry
==========
[![Build Status](https://travis-ci.org/conceptsandtraining/hug_sentry.svg?branch=master)](https://travis-ci.org/conceptsandtraining/hug_sentry)
[![Coverage Status](https://coveralls.io/repos/conceptsandtraining/hug_sentry/badge.svg?branch=master&service=github)](https://coveralls.io/github/conceptsandtraining/hug_sentry?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/conceptsandtraining/hug_sentry/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/conceptsandtraining/hug_sentry/?branch=master)

**hug_sentry** is a [Sentry](https://getsentry.com/) exception handler for the Python framework
[hug](https://github.com/timothycrosley/hug).

Installation
------------
Install via pip:

    pip install hug_sentry


Usage
-----
This is how you create a Redis store:

```python
from raven import Client
from hug_sentry import SentryExceptionHandler

# Create Raven client
client = Client('https://<key>:<secret>@app.getsentry.com/<project>')

# Create exception handler
handler = SentryExceptionHandler(client)

# Add to hug
__hug__.http.add_exception_handler(Exception, handler)
```

The arguments are as follows:

* **client**: A [Raven](https://pypi.python.org/pypi/raven) client object.

Remember that the `__hug__` object is only available after the first time a hug
decorator has been executed.

Authors
-------
**hug_sentry** is written and maintained by Fabian Kochem for CaT Concepts and Training GmbH.
