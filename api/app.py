#!/usr/bin/env python3
import uuid
from io import BytesIO
import os
from random import random, randint
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File
import uvicorn
import redis
from subprocess import Popen, PIPE

from starlette.responses import Response

app = FastAPI()
rdb = redis.Redis()


@app.get("/")
def read_root():
    return {"Hello": "World"}


HOUR = 3600
DAY = HOUR * 24
FLAMEGRAPH_TTL = DAY * 7

@app.get("/flame_graph/{key}")
def flame_graph_get(key: str):

    data = rdb.get("toolbox:FlameGraph:" + key)
    return Response(content=data, media_type="image/svg+xml")

@app.post("/flame_graph")
def flame_graph(file: bytes = File(...)):
    key = str(uuid.uuid4())
    temp = "/dev/shm/fg_%s.bin" % key
    with open(temp, "wb") as f:
        f.write(file)

    try:
        p1 = Popen(
            ["perf", "script", "-i", temp],
            stdout=PIPE, stderr=PIPE
        )

        p2 = Popen(
            ["perl", "stackcollapse-perf.pl"],
            cwd="./FlameGraph",
            stdin=PIPE, stdout=PIPE, stderr=PIPE,
        )

        p3 = Popen(
            ["perl", "flamegraph.pl"],
            cwd="./FlameGraph",
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )

        p2.stdin.write(p1.stdout.read())
        p2.stdin.close()

        p3.stdin.write(p2.stdout.read())
        p3.stdin.close()

        out = p3.stdout.read()
        rdb.set("toolbox:FlameGraph:" + key, out, ex=FLAMEGRAPH_TTL)

        return {
            "key": key,
            "script_err": p1.stderr.read().decode(),
            "fold_err": p2.stderr.read().decode(),
            "graph_err": p3.stderr.read().decode(),
        }
    finally:
        os.remove(temp)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
