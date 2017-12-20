#!/usr/bin/env python3

import requests
import re
import json
from urllib.parse import urljoin
from lxml import html


def channelVideos(channel):
	videoURL = 'https://www.youtube.com/' + channel
	# desktop browser useragent is required, otherwise youtube doesn't send the ytInitialData

	# attempt to find the data at least 3 times
	# because sometimes youtube mysteriously decides to send the bot-page for us
	for attempt_number in range(3):
		res = requests.get(videoURL, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/321 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'})
		# print(res.text)

		# tear out the json initalization data found in the page
		match = re.search(r'window\["ytInitialData"\]\s*=\s*(.*);\s*window\["ytInitialPlayerResponse"\]', res.text, re.MULTILINE)
		if match:
			json_data = match.group(1)
			data = json.loads(json_data)
			# print('got data:', data)
			tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
			for tab in tabs:
				if tab.get('tabRenderer') is not None and tab['tabRenderer']['title'] == "Videos":
					videos_tab = tab
					break
			else:
				raise Exception('no video tab found in ytInitialData')

			video_items = videos_tab['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
			videos = []
			for video_item in video_items:
				# print ('video:', video_item)

				title = video_item['gridVideoRenderer']['title']['simpleText']
				if video_item['gridVideoRenderer'].get('publishedTimeText') is not None:
					age = video_item['gridVideoRenderer']['publishedTimeText']['simpleText']
				else:
					age = '?'
				url = video_item['gridVideoRenderer']['navigationEndpoint']['webNavigationEndpointData']['url']
				link = urljoin(videoURL, url)

				# print('title:', title)
				# print('age:', age)
				# print('url:', url, link)

				# ignore videos with an unknown date
				if age != '?':
					videos.append({ 'link': link, 'title': title, 'age': age })

			return videos
		# else:
		# 	print('failed to find ytInitialData')

	raise Exception('failed to find ytInitialData')

# # old request function which doesnt work for youtube-red accounts
# def channelVideos(channel):
# 	videoURL = 'https://www.youtube.com/' + channel
# 	res = requests.get(videoURL)
# 	tree = html.fromstring(res.text)
# 	videos = []
# 	for videoItem in tree.xpath('//ul[@id = "channels-browse-content-grid"]/li'):
# 		videoLinkElement = videoItem.xpath('.//*[contains(@class, "yt-lockup-title")]/a')[0]
# 		link = urljoin(videoURL, videoLinkElement.xpath('./@href')[0])
# 		# print(link)
# 		title = videoLinkElement.xpath('./text()')[0]
# 		# print(title)

# 		videoMetaInfo = videoItem.xpath('.//ul[contains(@class, "yt-lockup-meta-info")]')[0]
# 		views = videoMetaInfo.xpath('./li[1]/text()')[0]
# 		age = videoMetaInfo.xpath('./li[2]/text()')[0]

# 		videos.append({ 'link': link, 'title': title, 'views': views, 'age': age })
# 	return videos

