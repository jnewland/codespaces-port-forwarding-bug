# GitHub Codespaces websocket bugs / limitations

* Connectivity fails for 1-5 minutes at startup due to improper `Origin` header on forwarded requests
* Max ~4 minute connection duration https://github.com/TrueBrain/codespaces-websocket

## Reproduction steps

- Create a new Codespace from this repo, using the latest VS Code Desktop or Web
- Run `python server.py`
- Open the URL it prints
  - The behavior doesn't seem to change if the port is public or private
- Observe the connectivity log in the web app
- Observe the connectivity log in terminal, notice the difference between the `Origin` header in the request received by the application over time

## Example

### Web connectivity log

```
Attempting to connect to websocket every 10s and send a ping every 30s ....

Thu Sep 22 2022 10:44:13 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:44:14 GMT-0500 (CDT) => Connection failed! 0.63 seconds since page load.
Thu Sep 22 2022 10:44:24 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:44:24 GMT-0500 (CDT) => Connection failed! 11.05 seconds since page load.
Thu Sep 22 2022 10:44:34 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:44:35 GMT-0500 (CDT) => Connection failed! 21.48 seconds since page load.
Thu Sep 22 2022 10:44:45 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:44:45 GMT-0500 (CDT) => Connection failed! 32.14 seconds since page load.
Thu Sep 22 2022 10:44:55 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:44:56 GMT-0500 (CDT) => Connection failed! 42.78 seconds since page load.
Thu Sep 22 2022 10:45:06 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:45:07 GMT-0500 (CDT) => Connection failed! 53.27 seconds since page load.
Thu Sep 22 2022 10:45:17 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:45:17 GMT-0500 (CDT) => Connection failed! 63.66 seconds since page load.
Thu Sep 22 2022 10:45:27 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:45:27 GMT-0500 (CDT) => Connection failed! 74.14 seconds since page load.
Thu Sep 22 2022 10:45:37 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:45:38 GMT-0500 (CDT) => Connection failed! 84.80 seconds since page load.
Thu Sep 22 2022 10:45:48 GMT-0500 (CDT) => Connecting to wss://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev/ws ...
Thu Sep 22 2022 10:45:49 GMT-0500 (CDT) => Connected 95.37 seconds after page load.
Thu Sep 22 2022 10:45:49 GMT-0500 (CDT) => pong in 126ms.
Thu Sep 22 2022 10:46:19 GMT-0500 (CDT) => pong in 128ms.
```

### Server request log

```
2022-09-22 15:44:13,750 <Request GET / > <Response OK eof> 0.00s
2022-09-22 15:44:14,332 <Request GET /ws > Origin=http://localhost
2022-09-22 15:44:14,332 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:44:24,748 <Request GET /ws > Origin=http://localhost
2022-09-22 15:44:24,749 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:44:35,153 <Request GET /ws > Origin=http://localhost
2022-09-22 15:44:35,154 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:44:45,865 <Request GET /ws > Origin=http://localhost
2022-09-22 15:44:45,866 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:44:56,479 <Request GET /ws > Origin=http://localhost
2022-09-22 15:44:56,479 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:45:06,979 <Request GET /ws > Origin=http://localhost
2022-09-22 15:45:06,979 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:45:17,391 <Request GET /ws > Origin=http://localhost
2022-09-22 15:45:17,391 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:45:27,793 <Request GET /ws > Origin=http://localhost
2022-09-22 15:45:27,794 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:45:38,507 <Request GET /ws > Origin=http://localhost
2022-09-22 15:45:38,508 <Request GET /ws > Bad Request 0.00s
2022-09-22 15:45:49,129 <Request GET /ws > Origin=https://jnewland-codespaces-websockets-bug-697p9g29wq-3000.githubpreview.dev
2022-09-22 15:45:49,130 <Request GET /ws > Connected!
```