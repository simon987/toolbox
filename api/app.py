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

from fastapi.params import Form
from starlette.responses import Response

app = FastAPI()
rdb = redis.Redis()


@app.get("/")
def read_root():
    return {"Hello": "World"}


TTL = 60 * 60


@app.get("/data/{key}")
def flame_graph_get(key: str, type: str):
    data = rdb.get("toolbox:data:" + key)
    return Response(content=data, media_type=type)


class SpectrographRequest:
    x: int
    y: int
    z: int
    label: str
    window: str

    def __init__(self, x, y, z, label, window, type):
        self.x = x
        self.y = y
        self.z = z
        self.label = label
        self.window = window
        self.type = type

    def valid(self):
        if self.x < 100 or self.x > 200000:
            return False

        if self.y < 100 or self.y > 10000:
            return False

        if self.z < 20 or self.z > 180:
            return False

        if self.window not in ("Hann", "Hamming", "Bartlett", "Rectangular", "Kaiser", "Dolph"):
            return False
        return True


@app.post("/spectrograph")
def spectrograph(file: bytes = File(...), x: int = Form(...), y: int = Form(...), z: int = Form(...), label=Form(...),
                 window=Form(...), type=Form(...)):
    key = str(uuid.uuid4())

    req = SpectrographRequest(x, y, z, label, window, type)
    if not req.valid():
        return {
            "err": "Invalid request"
        }

    p = Popen(
        ["sox",
         "-t", type,
         "-",
         "-n", "remix", "1", "spectrogram",
         "-t", label,
         "-x", str(x), "-y", str(y), "-z", str(z),
         "-w", window,
         "-o", "-"],
        stdin=PIPE, stdout=PIPE, stderr=PIPE,
    )

    p.stdin.write(file)
    p.stdin.close()

    out = p.stdout.read()
    rdb.set("toolbox:data:" + key, out, ex=TTL)

    return {
        "key": key
    }


@app.post("/flame_graph")
def flame_graph(file: bytes = File(...), width: int = 1200):
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
            ["perl", "flamegraph.pl", "--bgcolors", "#FFFFFF",
             "--fontsize", "10", "--fonttype", "monospace", "--width", str(width), "--title", " "],
            cwd="./FlameGraph",
            stdin=PIPE, stdout=PIPE, stderr=PIPE
        )

        p2.stdin.write(p1.stdout.read())
        p2.stdin.close()

        p3.stdin.write(p2.stdout.read())
        p3.stdin.close()

        out = p3.stdout.read()
        rdb.set("toolbox:data:" + key, out, ex=TTL)

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
