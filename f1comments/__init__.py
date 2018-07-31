import aiocache
import aiohttp

from sanic import Sanic, Blueprint
from sanic import response

from . import settings
from . import comments

app = Sanic(__name__)
api_v0 = Blueprint("v0", url_prefix="/v0")


Comments = comments.Comments()


@app.listener("before_server_start")
def setup_aioredis(sanic, loop):
    aiocache.caches.set_config(
        {
            "default": {
                "cache": "aiocache.RedisCache",
                "endpoint": settings.REDIS_HOST,
                "port": settings.REDIS_PORT,
                "namespace": "main",
                "serializer": {"class": "aiocache.serializers.PickleSerializer"},
            }
        }
    )


@api_v0.route("/ping")
async def ping(request):
    return response.json({"status": "ok"})


@api_v0.route("/comments")
async def serve_comments(request):
    resp = await get_comments()
    return response.json(resp)


@aiocache.cached(ttl=settings.TTL, key="f1comments_get_comments")
async def get_comments():
    try:
        return await Comments.get()
    except aiohttp.ClientError:
        await aiocache.caches.get("default").set("f1comments_get_comments", {}, ttl=60)
        return {}


app.blueprint(api_v0)
app.static("/", "f1comments/static/index.html")

def main():
    app.run(
        host="0.0.0.0",
        port=settings.PORT,
        workers=settings.WORKERS,
        debug=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
