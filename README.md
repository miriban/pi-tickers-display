# How to start:
## Using @pi2021_bot directly on telegram
You can directly use `@pi2021_bot` at telegram
to generate a code that can be used in the client
that you will have in your Raspberry PI.

## Using your own bot (optional)
You can try to build the code inside `firebase` 
directory but you need to do the following:
- Make sure you have `node` + `npm` version `12` installed
on your system.

- Setup new project at https://firebase.google.com/ and
install `firebase-tooling` into your system.

- Make sure to allow realtime database on firebase, it
follows the users that use your bot.

- You need to have a file called `.runtimeconfig.json`
inside the `firebase` directoy it should contain your
bot telegram token 
```json
    {
      "telegram": {
        "token": "YOUR_TELEGRAM_BOT_TOKEN"
      }
    }
```

- you can then run `npm i` and then 
`firebase serve --only hosting,functions` after 
authenticating your `firebase-tooling`.

- You can then use `ngrok` to serve your localhost
over internet.

- update your bot webhook uri.

- Bam! enjoy! now your bot can interact with multiple
users.

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
