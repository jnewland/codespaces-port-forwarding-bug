# GitHub Codespaces websocket bugs / limitations

* Max ~4 minute connection duration https://github.com/TrueBrain/codespaces-websocket
* Connectivity fails for 1-5 minutes at startup

## Reproduce

- Create a new codespace from this repo
- Run `python server.py`
- Open the URL it prints
- Observe the connectivity log

## Example

```
Attempting to connect to websocket every 10s and send a ping every 30s ....

Thu Sep 22 2022 09:53:03 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:53:04 GMT-0500 (CDT) => Connection failed! 0.66 seconds since page load.
Thu Sep 22 2022 09:53:14 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:53:14 GMT-0500 (CDT) => Connection failed! 11.26 seconds since page load.
Thu Sep 22 2022 09:53:24 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:53:25 GMT-0500 (CDT) => Connection failed! 21.76 seconds since page load.
Thu Sep 22 2022 09:53:35 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:53:35 GMT-0500 (CDT) => Connection failed! 32.16 seconds since page load.
Thu Sep 22 2022 09:53:45 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:53:47 GMT-0500 (CDT) => Connection failed! 43.36 seconds since page load.
Thu Sep 22 2022 09:53:57 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:53:57 GMT-0500 (CDT) => Connection failed! 53.74 seconds since page load.
Thu Sep 22 2022 09:54:07 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:54:07 GMT-0500 (CDT) => Connection failed! 64.19 seconds since page load.
Thu Sep 22 2022 09:54:17 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:54:18 GMT-0500 (CDT) => Connection failed! 74.63 seconds since page load.
Thu Sep 22 2022 09:54:28 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:54:28 GMT-0500 (CDT) => Connection failed! 85.07 seconds since page load.
Thu Sep 22 2022 09:54:38 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:54:39 GMT-0500 (CDT) => Connection failed! 95.58 seconds since page load.
Thu Sep 22 2022 09:54:49 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-g4wp4whwxvg-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 09:54:49 GMT-0500 (CDT) => Connected 106.16 seconds after page load.
Thu Sep 22 2022 09:54:50 GMT-0500 (CDT) => Ping/pong in 141ms.
Thu Sep 22 2022 09:55:20 GMT-0500 (CDT) => Ping/pong in 117ms.
```