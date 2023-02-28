# ETH Video Downloader

Python script to download videos from the ETH Zürich video portal, wrapped as Docker container. I use this personally to run it periodically on my Unraid server.

## Requirements:

- Docker

## Howto:

1. Clone this repo
2. Modify the `config.json` to add your courses and login credentials.
3. Run `docker build -t downloader .` to build the docker image.
4. Run `docker run -v $(pwd):/app downloader` to run the docker image.

## Options for config.json:

```json
    "redownload": "boolean value. If true, the script will redownload all videos, even if they already exist in the download folder.",
    "targets": [
        {
            "name":     "course name",
            "url":      "url to the course page on the video portal",
            "eth-login": "boolean value. If true, the login credentials are eth credentials, otherwise they should be special ones provided by the course instructor.",
            "username": "your username",
            "password": "your password"
        }
    ]
```

## Note:

If you have permission issues in the download folder after running this script, you can add ` && sudo chown $(whoami):$(whoami) -R *` at the end of the `docker run` command. This will change the permission of both user and group to the current user

## run.sh script:

You can also run the `run.sh` file, which will run the downloader for you (you still need to follow step 1 and 2 from the howto.

## Disclaimer:

This software is provided as is. I am not responsible for any damages on your system or legal actions brought forward against you. Only use it if you're allowed to save the videos on your hardware by ETH Zürich (http://www.video.ethz.ch/footer/copyright.html)

## Acknowledgements:

Thanks to [Pascal Wacker](https://github.com/pascalwacker/eth-video-downloader) for the original README.
