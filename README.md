rapidsms-envaya
===============

Backend for EnvayaSMS Android App

Installation
============

Check out http://rapidsms.readthedocs.org/en/latest/main/installation.html for how to install RapidSMS

then:

$ pip install git://github.com/dimagi/rapidsms-envaya.git

Add "envayasms" to INSTALLED_APPS

Add the following to INSTALLED_BACKENDS:

```
    'envayasms': {
        "ENGINE": "envayasms.backend",
        'port': 8880,
        'password': '1234',
        'url': 'http://10.0.2.2:8880',
        'max_delay': 60
    },
```

Of course, you'll probably want to modify that to your liking