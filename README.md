# discopusher 🕺

Easy triggers for Discord webhook

## How to use
- Create a TOML configuration file in the `./hooks` directory.
- Define your handlers and the webhooks that need to be triggered

Example:
`./hooks/from-shookaite.toml`
```toml
type = "twitter"
data = [
  "https://twitter.com/search?q=from%3AShookaite"
]
webhooks = [
  "Your Discord webhook"
]
# Optional
avatar_url = "a custom avatar"
# Optional
username = "a custom username"
```
Don't forget to fill your API keys in the `twitter.toml` file:
```toml
consumer = "xxxx"
consumer_secret = "xxxx"
access = "xxxx-xxxx"
access_secret = "xxxx"
```
You're ready to go! Now launch the script periodically, however you want.

Example:
```bash
while true; do
  python -m discopusher
  sleep 30m
done
```

## Current handlers

### Twitter
- Supports **Search**

Example:
`https://twitter.com/search?q=list%3Ashookaite%2Fvisual-artists%20filter%3Aimages%20-RT`
