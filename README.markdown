# aiotr

[![pypi](https://img.shields.io/pypi/v/aiotr.svg)](https://pypi.org/project/aiotr/)
![python](https://img.shields.io/pypi/pyversions/aiotr)
![implementation](https://img.shields.io/pypi/implementation/aiotr)
![wheel](https://img.shields.io/pypi/wheel/aiotr)
![license](https://img.shields.io/github/license/synodriver/aiotransmission.svg)

## The transmission python client with asyncio support

### simple usage

- add a torrent

```python
import asyncio
from pprint import pprint

import ujson
from aiotr import TransmissionClient


async def main():
    client = TransmissionClient(loads=ujson.loads, dumps=ujson.dumps)
    # client.host="xxx" needed when verify is enabled
    pprint(await client.port_test())
    data = await client.torrent_add(
        filename="magnet:?xt=urn:btih:091e5c8b3b3f4c4fac68c0867b4c5740365d79fb&dn=%5B210730%5D%5B%E9%88%B4%E6%9C%A8%E3%81%BF%E3%82%89%E4%B9%83%5D%E3%83%88%E3%82%A4%E3%83%AC%E3%81%AE%E8%8A%B1%E5%AD%90%E3%81%95%E3%82%93VS%E5%B1%88%E5%BC%B7%E9%80%80%E9%AD%94%E5%B8%AB%20%EF%BD%9E%E6%82%AA%E5%A0%95%E3%81%A1%E3%83%9E%E2%97%8B%E3%82%B3%E3%81%AB%E5%A4%A9%E8%AA%85%E3%82%B6%E3%83%BC%E3%83%A1%E3%83%B3%E9%80%A3%E7%B6%9A%E4%B8%AD%E5%87%BA%E3%81%97%EF%BD%9E%20%E7%AC%AC%E4%B8%89%E6%80%AA%EF%BC%88%E3%81%A0%E3%81%84%E3%81%95%E3%82%93%E3%81%8B%E3%81%84%EF%BC%89%20%E6%88%A6%E6%85%84%E3%80%8E%E4%BA%BA%E9%9D%A2%E7%8A%AC%E3%80%8F%EF%BC%81%E5%81%A5%E5%BA%B7%E5%84%AA%E8%89%AF%E7%8A%AC%E8%80%B3%E2%97%8B%E5%A5%B3%E3%81%AB%E5%88%9D%E3%82%81%E3%81%A6%E3%81%AE%E6%80%A7%E6%95%99%E8%82%B2%28No%20Watermark%29.mp4&tr=http%3A%2F%2Fsukebei.tracker.wf%3A8888%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce")
    pprint(data)


asyncio.run(main())
```
Rpc methods are listed [here](https://github.com/transmission/transmission/blob/master/extras/rpc-spec.txt)
