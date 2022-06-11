# GitHub Codespaces websocket timeout

Websockets on GitHub Codespaces consistently close after ~4 minutes after being established.

This problem only seem to exist on GitHub Codespaces, and seems to be related to their webproxy.
When trying alternatives to GitHub Codespaces (like Gitpod), we do not see this issue.
When trying alternatives to their webproxy (like ngrok), we also do not see this issue.

The problem exists for both Private and Public ports.
The problem exists with regular ping/pong messages or no messages at all.
The problem is also very consistent: it never disconnects before the 4 minute mark, and always shortly after (sometimes on the dot, sometimes with a few seconds drift).

This all combined gives the suspicion that this is a configuration on the GitHub webproxy, to disconnect any still-open connection after 4 minutes.
This seems to forget the fact websockets exist in this world :)

The main issue with this disconnect is that a lot of web frameworks use a websocket during development to live-update the website, to make development a smooth experience.
This disconnect every ~4 minutes kinda ruins that experience, as often web frameworks do a full reload after the websocket connection is lost.

This repository is meant to make it easy to reproduce this issue for everyone with access to GitHub Codespaces.

## Getting started

Open this repository in Codespaces.

```bash
python server.py
```

Click on the `Open in Browser` button that now pops up.

Wait ~4 minutes, and see `Connection lost!` message.
You can press `Retry` to retry the test, and after 4 minutes you will see the `Connection lost!` message again.
Consistently.
Always.

## Alternatives tried

- `Gitpod`: no disconnects any after measurable time.
- `ngrok`: no disconnects any after measurable time.
- `nodejs` as server: no difference.
- `Private` vs `Public` port: no difference.
- `Firefox` and `Chrome`: no difference.
- Ping every 1 second: no difference.
- No communication over websocket: no difference.
