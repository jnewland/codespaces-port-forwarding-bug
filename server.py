import aiohttp
import logging
import os

from aiohttp import web

routes = web.RouteTableDef()


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
    <title>Websocket connectivity debug log</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
</head>
 
<body>
    <div class="container">
        <h1>Websocket connectivity debug log</h1>
        <p><a href="https://github.com/jnewland/codespaces-websockets-bug">https://github.com/jnewland/codespaces-websockets-bug</a></p>
        <p>
            Attempting to connect to websocket every 10s and send a ping every 30s ...
        </p>

        <pre id="info">
            Loading ...
        </pre>

    </div>
</body>
 
<script>
    function log(string) {
        document.getElementById("info").innerHTML += new Date() + " => " + string + "<br />";
    }
    let loadDate = new Date();
    let connected = false;
    function StartTest() {
        let startDate = new Date();
        let pingDate;

        const url = "wss://" + window.location.host + "/ws";
        log("Connecting to " + url + " ...");

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

        socket.addEventListener("close", function (event) {
            if (connected) {
                log("Connection lost! Connected " + ((new Date().getTime() - startDate.getTime()) / 1000).toFixed(2) + " seconds.");

                clearTimeout(timeout);

                timeout = setTimeout(() => {
                    StartTest();
                }, 1000);

            } else {
                log("Connection failed! " + ((new Date().getTime() - loadDate.getTime()) / 1000).toFixed(2) + " seconds since page load.");

                timeout = setTimeout(() => {
                    StartTest();
                }, 10000);
            }

        });

        socket.addEventListener("message", function (event) {
            log("Ping/pong in " + ((new Date().getTime() - pingDate.getTime())).toFixed(0) + "ms.");

            timeout = setTimeout(() => {
                pingDate = new Date();
                socket.send("ping");
            }, 30000);
        });
    }

    document.getElementById("info").innerHTML = "";
    StartTest();
</script>
 
</html>
""",
    )


@routes.get("/ws")
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT and msg.data == "ping":
            await ws.send_str("pong")

    return ws


app = web.Application()
app.add_routes(routes)
logging.basicConfig(level=logging.DEBUG)

print("")
print("Open the following link to replicate the bug:")
print("")
print("  https://{}-3000.githubpreview.dev/".format(os.getenv("CODESPACE_NAME")))
print("")

web.run_app(app, port=3000)
