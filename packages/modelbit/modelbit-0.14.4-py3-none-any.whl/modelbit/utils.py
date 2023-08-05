from typing import Union, Any, cast, Dict, Callable, Tuple
from datetime import datetime
import os, re, pickle, gzip, hashlib
import time

_deserializeCache: Dict[str, Any] = {}


# From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeOfFmt(num: Union[int, Any]):
  if type(num) != int:
    return ""
  numLeft: float = num
  for unit in ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
    if abs(numLeft) < 1000.0:
      return f"{numLeft:3.0f} {unit}"
    numLeft /= 1000.0
  return f"{numLeft:.1f} YB"


def pandasTypeToPythonType(pandasType: str):
  if pandasType in ['float32', 'float64']:
    return 'float'
  if pandasType in ['int32', 'int64']:
    return 'int'
  if pandasType == 'bool':
    return 'bool'
  return 'Any'


def simplifyArgName(argName: str):
  scrubbed = re.sub("\\W+", "_", argName.lower())
  scrubbed = re.sub('^(\\d+)', "c\\1", scrubbed)
  if scrubbed.endswith("_"):
    scrubbed = scrubbed[:-1]
  return scrubbed


def unindent(source: str) -> str:
  leadingWhitespaces = len(source) - len(source.lstrip())
  if leadingWhitespaces == 0:
    return source
  newLines = [line[leadingWhitespaces:] for line in source.split("\n")]
  return "\n".join(newLines)


def timeago(pastDateMs: int):
  nowMs = time.time() * 1000
  options = [
      {
          "name": "second",
          "divide": 1000
      },
      {
          "name": "minute",
          "divide": 60
      },
      {
          "name": "hour",
          "divide": 60
      },
      {
          "name": "day",
          "divide": 24
      },
      {
          "name": "month",
          "divide": 30.5
      },
  ]
  currentDiff = nowMs - pastDateMs
  if currentDiff < 0:
    raise Exception("The future is NYI")
  resp = "Just now"
  for opt in options:
    currentDiff = round(currentDiff / cast(Union[float, int], opt["divide"]))
    if currentDiff <= 0:
      return resp
    pluralS = ""
    if currentDiff != 1:
      pluralS = "s"
    resp = f"{currentDiff} {opt['name']}{pluralS} ago"
  return resp


def deserializeGzip(contentHash: str, reader: Callable[..., Any]):
  if contentHash not in _deserializeCache:
    _deserializeCache[contentHash] = pickle.loads(gzip.decompress(reader()))
  return _deserializeCache[contentHash]


def serializeZstd(obj: Any) -> Tuple[bytes, str, int]:
  # zstd is not available in snowpark, so move the import here. Can change once we no longer need modelbit in snowpark
  import zstd  # type:ignore
  pklData = pickle.dumps(obj)
  contentHash = f"sha1:{hashlib.sha1(pklData).hexdigest()}"
  objSize = len(pklData)
  compressedPickle = cast(bytes, zstd.compress(pklData, 10))  # type: ignore
  return (compressedPickle, contentHash, objSize)


def timestamp():
  return int(datetime.timestamp(datetime.now()) * 1000)


def getEnvOrDefault(key: str, defaultVal: str) -> str:
  osVal = os.getenv(key)
  if type(osVal) == str:
    return str(osVal)
  else:
    return defaultVal


def inDeployment() -> bool:
  return 'WORKSPACE_ID' in os.environ
