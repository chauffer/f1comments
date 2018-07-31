import os
import multiprocessing

api_version = "v0"

PORT = int(os.getenv("F1COMMENTS_PORT", "80"))
WORKERS = int(os.getenv("F1COMMENTS_WORKERS", multiprocessing.cpu_count()))
DEBUG = os.getenv("F1COMMENTS_DEBUG") is not None

REDIS_HOST = os.getenv("F1COMMENTS_REDIS_HOST", "redis")
REDIS_PORT = os.getenv("F1COMMENTS_REDIS_PORT ", "6379")

TTL = int(os.getenv("F1COMMENTS_TTL", "2"))
