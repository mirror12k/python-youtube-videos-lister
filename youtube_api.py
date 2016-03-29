#!/usr/bin/env python3

import requests



res = requests.get('https://www.youtube.com/user/TeamFortressTV/videos')

print (res.text)
