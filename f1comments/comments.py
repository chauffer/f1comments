import json
import time

import aiohttp
from pyjsparser import PyJsParser


class Comments:
    def __init__(self, timeout_s=5):
        self.timeout_s = timeout_s

        self.session = None
        self.p = PyJsParser()

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
            "https://www.formula1.com/sp/static/f1/2018/serverlist/svr/serverlist.xml.js",
            params=self.params,
        ) as r:
            parsed = self.p.parse(await r.text())["body"]

        for x in parsed:
            try:
                if x["declarations"][0]["id"]["name"] == "svr":
                    target = x["declarations"][0]["init"]["name"]
            except:
                pass

        info = {
            k2["key"]["name"]: k2["value"]["value"]
            for k2 in [
                k
                for k in [
                    x
                    for x in parsed
                    if "declarations" in x
                    and x["declarations"][0]["id"]["name"] == target
                ][0]["declarations"][0]["init"]["properties"]
            ]
            if k2["key"]["name"] in ("race", "session")
        }

        url = "https://lb.softpauer.com/f1/2018/live/{race}/{session}/".format(**info)

        async with self.session.get(url + "/com.en.js", params=self.params) as r:
            r_comms = await r.text()
        async with self.session.get(url + "/com.rc.js", params=self.params) as r:
            r_racecontrol = await r.text()

        comms = json.loads(r_comms[5:-2])["feed"]["e"]
        racecontrol = json.loads(r_racecontrol[5:-2])["feed"]["e"]

        return {"info": info, "comms": comms, "racecontrol": racecontrol}
