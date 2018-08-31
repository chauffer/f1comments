import codecs
import json
import time

import aiohttp


class Comments:
    def __init__(self, timeout_s=5):
        self.timeout_s = timeout_s
        self.session = None
        self.CDN = "https://livetiming.formula1.com/static/"

    @property
    def params(self):
        return {"t": int(time.time())}

    async def get(self):
        if not self.session:
            self.session = aiohttp.ClientSession(
                raise_for_status=True,
                timeout=aiohttp.ClientTimeout(
                    connect=self.timeout_s, total=self.timeout_s * 2
                ),
            )

        async with self.session.get(
            self.CDN + "SessionInfo.json", params=self.params
        ) as r:
            res = await r.read()
            self.metadata = json.loads(codecs.decode(res, "utf-8-sig"))

        async with self.session.get(
            self.CDN + self.metadata["Path"] + "com.en.js", params=self.params
        ) as r:
            r_comms = await r.text()
        async with self.session.get(
            self.CDN + self.metadata["Path"] + "com.rc.js", params=self.params
        ) as r:
            r_racecontrol = await r.text()

        comms = json.loads(r_comms[5:-2])["feed"]["e"]
        racecontrol = json.loads(r_racecontrol[5:-2])["feed"]["e"]

        return {"metadata": self.metadata, "comms": comms, "racecontrol": racecontrol}
