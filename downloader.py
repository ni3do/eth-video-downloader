import asyncio
import json
import os
import urllib
from datetime import datetime

import aiohttp
import requests
from discord import Embed, Webhook


async def main():
    config = json.load(open("config.json"))
    date_format = "%Y%m%d"

    for target in config["targets"]:
        print(f"Downloading {target['name']}")

        s = requests.Session()
        s.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
        s.headers["Host"] = "video.ethz.ch"
        s.headers["DNT"] = "1"
        s.headers["Upgrade-Insecure-Requests"] = "1"

        base_url = target["url"].rsplit(".", 1)[0]

        if target["eth-login"]:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-GB,en;q=0.5",
                # 'Accept-Encoding': 'gzip, deflate, br',
                "CSRF-Token": "undefined",
                "Origin": "https://video.ethz.ch",
                "DNT": "1",
                "Connection": "keep-alive",
                "Referer": target["url"],
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }

            data = {
                "_charset_": "utf-8",
                "j_username": target["username"],
                "j_password": target["password"],
                "j_validate": "true",
            }

            sec_check_url = base_url + "/j_security_check"
            response = s.post(sec_check_url, headers=headers, data=data)
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-GB,en;q=0.5",
                # 'Accept-Encoding': 'gzip, deflate, br',
                "CSRF-Token": "undefined",
                "Origin": "https://video.ethz.ch",
                "DNT": "1",
                "Connection": "keep-alive",
                "Referer": target["url"],
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }

            data = {
                "_charset_": "utf-8",
                "username": target["username"],
                "password": target["password"],
            }

            sec_check_url = base_url + ".series-login.json"
            response = s.post(sec_check_url, headers=headers, data=data)

        print(f"Login status: {response.status_code} {response.reason}")

        series_metadata = json.loads(s.get(base_url + ".series-metadata.json").text)
        episodes = series_metadata["episodes"]
        for idx, ep in enumerate(episodes):
            iso_date = datetime.fromisoformat(ep["createdAt"])
            file_name = (
                target["name"]
                + "_"
                + str(len(episodes) - idx)
                + "_"
                + datetime.strftime(iso_date, date_format)
                + ".mp4"
            )
            if (not os.path.exists(target["name"] + "/" + file_name)) or config["redownload"]:
                if not os.path.exists(target["name"]):
                    os.mkdir(target["name"])
                ep_metadata = json.loads(
                    s.get(base_url + "/" + ep["id"] + ".series-metadata.json").text
                )
                video_url = ep_metadata["selectedEpisode"]["media"]["presentations"][0]["url"]
                print(f"Downloading {file_name} ({idx+1}/{len(episodes)}) from {video_url}")
                urllib.request.urlretrieve(video_url, target["name"] + "/" + file_name)
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(config["webhook"], session=session)
                    embed = Embed()
                    embed.add_field(name="Subject", value=target["name"])
                    embed.add_field(name="Episode", value=len(episodes) - idx)
                    embed.add_field(
                        name="Uploaded", value=datetime.strftime(iso_date, "%H:%M %d.%m.%Y")
                    )
                    await webhook.send(embed=embed, username="ETH Video Downloader")
            else:
                print(f"Skipping {file_name} ({idx+1}/{len(episodes)})")
        s.close()


asyncio.run(main())
