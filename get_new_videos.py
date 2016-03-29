#!/usr/bin/env python3

import youtube_api
import re
import sys



def parseTime(time):
	match = re.match(r'^(\d+) (second|minute|hour|day|week|month|year)s? ago$', time)
	if match is None:
		raise Exception("invalid time given: '"+time+'"')
	else:
		value = int(match.group(1))
		if match.group(2) == 'minute':
			value *= 60
		elif match.group(2) == 'hour':
			value *= 60 * 60
		elif match.group(2) == 'day':
			value *= 60 * 60 * 24
		elif match.group(2) == 'week':
			value *= 60 * 60 * 24 * 7
		elif match.group(2) == 'month':
			value *= 60 * 60 * 24 * 30
		elif match.group(2) == 'year':
			value *= 60 * 60 * 24 * 365
		return value



def getRecent(channel, time):
	timeFrame = parseTime(time)

	return [ video for video in youtube_api.channelVideos(channel) if parseTime(video['age']) <= timeFrame ]





if __name__ == '__main__':
	time = sys.argv[1]
	for channel in [
		'user/TeamFortressTV/videos',
	]:
		videos = getRecent(channel, time)
		if len(videos) > 0:
			print('[['+channel+']]:')
			for video in videos:
				print('\t"'+video['title']+'" -', video['link'], '- (', video['age'], ')')

