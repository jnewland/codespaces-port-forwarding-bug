import aiohttp
import logging
import os

from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/auth/test")
async def auth_test(request):
    return web.json_response({'status': 'ok'})

@routes.get("/")
async def hello(request):
    return web.Response(
        content_type="text/html",
        text="""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Port forwarding connectivity debug log</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
</head>
 
<body>
    <div class="col mx-auto p-4 py-md-5">
        <div class="row g-5">
            <h1>Port forwarding connectivity debug log</h1>
            <p><a href="https://github.com/jnewland/codespaces-websockets-bug">https://github.com/jnewland/codespaces-websockets-bug</a></p>
        </div>
        <div class="row g-5">
            <div class="col-md-6">
                <h3>Websocket</h3>
                <p>Attempts to connect to websocket every 10s and send a ping every 30s</p>
                <div class="bg-light p-3 mb-2">
                    <samp id="info" class="small">
                        Loading ...
                    </samp>
                </div>
            </div>
            <div class="col-md-6">
                <h3>HTTP /auth</h3>
                <p>Attempts to perform `GET /auth/test` every 10s</p>
                <div class="bg-light p-3 mb-2">
                    <samp id="auth" class="small">
                        Loading ...
                    </samp>
                </div>
            </div>
        </div>
    </div>
</body>
 
<script>
    function log(string, div="info") {
        document.getElementById(div).innerHTML += new Date() + " => " + string + "<br />";
    }
    let loadDate = new Date();
    let connected = false;
    function StartTest() {
        let startDate = new Date();
        let pingDate;

        const url = "wss://" + window.location.host + "/ws";
        log("Connecting to " + url + " ...");

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    log("/auth/test " + this.status + ": " + xhttp.responseText + " " + xhttp.getAllResponseHeaders(), "auth")

                    timeout = setTimeout(() => {
                        log("Get /auth/test ...", "auth");
                        xhttp.open("GET", "/auth/test", true);
                        xhttp.send();
                    }, 10000);
                } else {
                    log("/auth/test " + this.status + " " +xhttp.getAllResponseHeaders(), "auth")
                }
            }
        };
        log("Get /auth/test ...", "auth");
        xhttp.open("GET", "/auth/test", true);
        xhttp.send();

        const socket = new WebSocket(url);
        let timeout;

        socket.addEventListener("open", function (event) {
            connected = true;
            log("Connected " + ((new Date().getTime() - loadDate.getTime()) / 1000).toFixed(2) + " seconds after page load.");
            // Cancel any old pings.
            clearTimeout(timeout);

            pingDate = new Date();
            socket.send("ping");
        });

        socket.addEventListener("error", function (event) {
            console.log(event)
            log("Error. Connected " + ((new Date().getTime() - startDate.getTime()) / 1000).toFixed(2) + " seconds.");
        });

        socket.addEventListener("close", function (event) {
            console.log(event)
            if (connected) {
                log("Connection failed. Connected " + ((new Date().getTime() - startDate.getTime()) / 1000).toFixed(2) + " seconds.");

                clearTimeout(timeout);

                timeout = setTimeout(() => {
                    StartTest();
                }, 1000);

            } else {
                log("Connection failed: " + ((new Date().getTime() - loadDate.getTime()) / 1000).toFixed(2) + " seconds since page load.");

                timeout = setTimeout(() => {
                    StartTest();
                }, 10000);
            }
            connected = false;
        });

        socket.addEventListener("message", function (event) {
            log(event.data + " in " + ((new Date().getTime() - pingDate.getTime())).toFixed(0) + "ms.");

            timeout = setTimeout(() => {
                pingDate = new Date();
                socket.send("ping");
            }, 30000);
        });
    }

    document.getElementById("info").innerHTML = "";
    document.getElementById("auth").innerHTML = "";
    StartTest();
</script>
 
</html>
"""
    )


@routes.get("/ws")
async def websocket_handler(request):
    origin = request.headers["Origin"]
    logging.debug(f"<Request GET /ws > Origin={origin}")
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    logging.debug(f"<Request GET /ws > Connected!")

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT and msg.data == "ping":
            await ws.send_str("pong")

    return ws


app = web.Application()
app.add_routes(routes)

from aiohttp.abc import AbstractAccessLogger


class AccessLogger(AbstractAccessLogger):
    def log(self, request, response, time):
        self.logger.info(f"{request} {response} %.2fs" % time)


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")

print("")
print("Open the following link to replicate the bug:")
print("")
print("  https://{}-3000.githubpreview.dev/".format(os.getenv("CODESPACE_NAME")))
print("")

web.run_app(app, port=3000, access_log_class=AccessLogger)
