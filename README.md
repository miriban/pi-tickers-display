## Monitor ETFs Portfolio on a Raspberry pi display

Telegram Bot name is `pi2021_bot`.The following 
commands are supported:

- `/start` it will generate a user id in order to
be able to connect your `client` to the server.

- `/add btc amzn goog` to add one or multiple etfs
tikers. They will be added to the begining of the 
tickers list.

- `/remove amzn goog` to remove one or multiple
etfs tickers. They will be automatically removed
from the list.

- `/move amzn 1` to move a certain ticker into
certain position.

---

### Starting Client on Rasperry PI

- Run `pip install -r requirements.txt` to install
required python libs.

- Create an account at http://twelvedata.com and get
your api key.

- Create a file named `apis.tmp` and insert the 
following
```json
{
    "twelveDataApiKey": "YOUR_TWELVE_DATA_API_KEY"
}
```

- Run `python3 app.py`
