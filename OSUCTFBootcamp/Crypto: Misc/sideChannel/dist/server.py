from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import os
from pathlib import Path
import subprocess
import string
from typing import Optional
from fastapi.staticfiles import StaticFiles
import time
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
flag = open("flag.txt").read()


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/run/")
def run(code: str, response: Response):
    basename = hex(random.randrange(0x100000000))[2:]

    compiler_output = compile(basename, code)

    filepath = Path("/opt/transfer") / basename
    if not filepath.is_file():
        response.status_code = 400
        return compiler_output

    elapsed = run_bin(filepath, flag)
    return elapsed


def compile(basename: str, src: str) -> str:
    with open(f"/opt/transfer/{basename}.c", "w") as f:
        f.write(src)

    cmd = f"/opt/jailyard/compile.sh {basename}"
    res = subprocess.run(
        f'/opt/app/run_jail.sh /opt/app/jails/gcc.cfg "{cmd}"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    return res.stdout.decode()


def run_bin(filepath: Path, flag: str) -> float:
    cmd = f"{filepath} {flag}"
    start = time.time()
    subprocess.run(
        f'/opt/app/run_jail.sh /opt/app/jails/bin.cfg "{cmd}"',
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    return time.time() - start
