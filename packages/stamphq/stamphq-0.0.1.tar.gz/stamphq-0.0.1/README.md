### stampHQ-python SDK

This SDK lets you interact with stampHQ APIs with python. The SDK currently supports mail sending.

### Install
```shell
pip install stamphq
```

### Usage
You need a [stamphq](https://www.stamphq.app) account. Signup for an account [here](https://dash.stamphq.app/signup)
to obtain an API key.

```python
from stamphq.client import StampHQClient

# create the client
client = StampHQClient(api_key="<key obtained from dashboard>")

# send email with text and html parts
message_id = client.send_email(
    sender="catelyn@winterfell.com",
    to=["ned@winterfell.com"],
    subject="Regarding Jon Snow!",
    text_content="I know about Jon Snow Ned.",
    html_content="<html><body><p>I know about Jon Snow Ned. <i>And, be careful with Lannisters.</i></p></body></html>",
)
print(message_id) # prints the Message-ID for the email.
```

#### TODO
- [ ] add template support

#### Support
please write to `sdk@stamphq.app`
