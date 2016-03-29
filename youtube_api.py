#!/usr/bin/env python3

import requests
from urllib.parse import urljoin
from lxml import html


def channelVideos(channel):
	videoURL = 'https://www.youtube.com/' + channel
	res = requests.get(videoURL)
	tree = html.fromstring(res.text)
	videos = []
	for videoItem in tree.xpath('//ul[@id = "channels-browse-content-grid"]/li'):
		videoLinkElement = videoItem.xpath('.//*[contains(@class, "yt-lockup-title")]/a')[0]
		link = urljoin(videoURL, videoLinkElement.xpath('./@href')[0])
		title = videoLinkElement.xpath('./text()')[0]
		# print(link, title)
		videoMetaInfo = videoItem.xpath('.//ul[contains(@class, "yt-lockup-meta-info")]')[0]
		views = videoMetaInfo.xpath('./li[1]/text()')[0]
		age = videoMetaInfo.xpath('./li[2]/text()')[0]
		# print(views, age)
		videos.append({ 'link': link, 'title': title, 'views': views, 'age': age })
	return videos

# print(channelVideos('user/TeamFortressTV/videos'))
