rapidsms-envaya
===============

Backend for EnvayaSMS Android App

Installation
============

Check out http://rapidsms.readthedocs.org/en/latest/main/installation.html for how to install RapidSMS.

Then, in your project directory:

```
$ git clone git://github.com/dimagi/rapidsms-envaya.git
```

In settings.py:

Add `"rapidsms-envaya"` to the list `INSTALLED_APPS`.

Add the following to `INSTALLED_BACKENDS`:

```
    'envayasms': {
        "ENGINE": "rapidsms-envaya.backend",
        'port': 8880, # feel free to change the port
        'password': None, # set to a string to set the password
        'url': 'http://10.0.2.2:8880/', # important: this must exactly match what is entered in your Android phone
        'max_delay': None
    }
```

`max_delay` is the number of seconds before RapidSMS will send messages to the wrong country code. By default, RapidSMS will only return messages to phones in the country that the EnvayaSMS instance uses. If you set max_delay to an integer, it will return messages to phones in other countries as a back-up in case there are no EnvayaSMS phones in the country the message is being sent to. This may cost a lot of money, since international texting is expensive. You can set `max_delay` to 0 to automatically send all messages to the first phone that checks for new messages.

Finally, set up EnvayaSMS on an Android phone. See http://sms.envaya.org/install/ for how to install EnvayaSMS on a real phone, or http://sms.envaya.org/test/ for how to test on your local machine. EnvayaSMS has some great documentation on how to further set up EnvayaSMS--this guide will only tell you the bare minimum.

Once you have EnvayaSMS running, set URL to point to the machine running RapidSMS, matching exactly the URL set above. Do the same with the password, if it is set in RapidSMS. (The password feature won't work unless you set the URL correctly.)

And now enjoy sending SMSes through EnvayaSMS!
