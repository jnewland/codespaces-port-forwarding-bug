import aiohttp

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def hello(request):
    return web.Response(
        content_type="text/html",
        text="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Codespaces Websocket Test</title>
</head>
 
<body>
    <div>
        This page will make a websocket connection to the server, and send a ping every 30 seconds.<br/>
        It will tell you when the websocket connection is lost, and how much time there was between connect and disconnect.
    </div>

    <div id="info">
        Loading ...
    </div>

    <button id="retry" onclick="StartTest()">Retry</button>
</body>
 
<script>
    function StartTest() {
        let startDate;

        document.getElementById("info").innerHTML += "<br />" + new Date() + " => " + "Connecting ...";
        // Hide the retry button for as long as we are connecting / connected.
        document.getElementById("retry").style = "display: none;";

        const url = "wss://" + window.location.host + "/ws";
        const socket = new WebSocket(url);
        let timeout;

        socket.addEventListener("open", function (event) {
            startDate = new Date();
            document.getElementById("info").innerHTML += "<br />" + new Date() + " => " + "Connected";
            socket.send("ping");
        });

        socket.addEventListener("close", function (event) {
            document.getElementById("info").innerHTML += "<br />" + new Date() + " => " + "Connection lost!";

            // Cancel the ping.
            clearTimeout(timeout);

            // Show the time we were connected.
            document.getElementById("info").innerHTML += "<br /><br />Time between connect and disconnect: " + ((new Date().getTime() - startDate.getTime()) / 1000 / 60).toFixed(2) + " minutes<br />";

            // Show a button you can press to start again. Avoids page reloads.
            document.getElementById("retry").style = "display: block;";
        });

        socket.addEventListener("message", function (event) {
            document.getElementById("info").innerHTML += "<br />" + new Date() + " => Ping/pong";

            // Repeat the ping every 30 seconds to keep the websocket alive.
            timeout = setTimeout(() => {
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
web.run_app(app, port=3000)
