import asynchttpserver
import asyncdispatch
import json
import osproc
import cgi
import uri
import tables
import logging
import strformat
import sequtils
import strutils
import random

proc parseQueryString*(req: Request): Table[string, string] =
  ## Parse a query string like ``foo=bar&baz=5`` into
  ## ``{"foo": "bar", "baz": "5"}``
  result = initTable[string, string]()
  let query = req.url.query

  try:
    for key, val in cgi.decodeData(query):
      result[key] = val
  except CgiError:
    logging.warn(fmt"Incorrect query. Got: {query}")

proc randomString(n: int): string =
  newSeqWith(n, HexDigits.sample()).join()

proc compileCode(code: string): string =
  ## Compile code into a random file in `/opt/box`. Set privileges to `nimc`
  ## user for SECURITY REASONS. Returns the filename if it compiled properly.
  result = fmt"/opt/box/{randomString(8)}"
  let (output, exit_code) = execCmdEx(
    fmt"su - nimc -c 'nim compile -o:{result} -'",
    input = code
  )
  if exit_code != 0:
    raise newException(ValueError, output)

proc runCode(code: string): string =
  ## Compile the code, then run it in nsjail for SECURITY REASONS.
  let file = compileCode(code)
  var (output, _) = execCmdEx(fmt"/opt/app/run_jail.sh {file}")
  return output

proc main {.async.} =
  var server = newAsyncHttpServer()
  proc cb(req: Request) {.async.} =
    let headers = newHttpHeaders([("Content-Type","application/json")])
    debug(fmt"Request: {$req.url}")

    if req.url.path == "/api/run":

      let params = parseQueryString(req)
      if "code" in params and params["code"].len() < 1024:
        let code = params["code"]
        debug(fmt"Running: {code}")

        try:
          let output = runCode(code)
          let msg = %* {"output": output}
          await req.respond(Http200, $msg, headers)
        except:
          let msg = %* {"error": getCurrentExceptionMsg()}
          await req.respond(Http400, $msg, headers)

      else:
        let msg = %* {"error": "Invalid parameters"}
        await req.respond(Http400, $msg, headers)

    else:
      let msg = %* {"msg": "Not found"}
      await req.respond(Http404, $msg, headers)

  server.listen Port(5555)
  while true:
    if server.shouldAcceptRequest():
      await server.acceptRequest(cb)
    else:
      poll()

addHandler(newConsoleLogger())
info("Starting server")
randomize()
asyncCheck main()
runForever()
