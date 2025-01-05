from datetime import datetime, timedelta
import json
import os

rootdir = 'raw/post-data'
chatdir = f'{rootdir}/liveChat'


def get_post_dict():
	post_dict = dict()

	with open(f'{rootdir}/all_live_posts.json', 'r') as file:
		all_post_data = json.load(file)  # print(all_post_data[0])
		for post_data in all_post_data:
			# if not 'drmStatus' in post_data['extension']['video']:
			# 	continue
			post_dict[post_data['postId']] = post_data  # else:  # 	print('skip')
	return post_dict


def get_chat_data(f):
	with open(f'{chatdir}/{f}', 'r') as file:
		data = json.load(file)

	def sort(d):
		return d['messageTime']

	data = sorted(data, key=sort)
	return data


def timedelta_to_vtt_format(td: timedelta) -> str:
	total_seconds = int(td.total_seconds())
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
	milliseconds = td.microseconds // 1000
	return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"


def get_datetime(timestamp) -> datetime:
	time = int(timestamp) / 1000
	return datetime.fromtimestamp(time)


def main():
	post_dict = get_post_dict()

	for f in os.listdir(chatdir):
		# print(f)

		post_id = f.rsplit('.')[0]

		if post_id not in post_dict:
			continue

		# if post_id != '1-109612923':
		# 	continue

		start_time = post_dict[post_id]['extension']['video']['onAirStartAt']
		# print('start time', start_time)

		start_datetime: datetime = get_datetime(start_time)

		data = get_chat_data(f)

		# with open(f'{chatdir}/{f}', 'r') as file:

		out = []
		skip_next = False
		for i, d in enumerate(data):

			if skip_next:
				skip_next = False
				continue

			time = d['messageTime']
			name = d['profile']['profileName']
			msg = d['content']

			sub_datetime = get_datetime(time)
			start_delta: timedelta = sub_datetime - start_datetime

			duration = 3.5
			if len(msg) < 10:
				duration = 3
			elif len(msg) > 35:
				duration = 7
			else:
				duration = 5

			body = f'{name}: {msg}'

			if i < len(data) - 1:
				next = data[i + 1]
				next_sub_start = get_datetime(next['messageTime'])
				# print(next_sub_start)
				# print(sub_datetime)
				delta = next_sub_start - sub_datetime

				next_name = next['profile']['profileName']
				next_msg = next['content']

				delta_seconds = delta.total_seconds()
				if delta_seconds < 0.5:
					skip_next = True
					if next_msg != msg:
						body = f'{name}: {msg}\n{next_name}: {next_msg}'
						print('merged')
						print(body)
						duration = 4
				elif delta_seconds < duration:
					duration = delta_seconds - 0.01
					print('Set duration to ', duration)

			end_delta: timedelta = start_delta + timedelta(seconds=duration)

			if '\n' in msg:
				print(msg)
				breakpoint()

			# print(f'{start_datetime} {name}: {msg}')
			line = f'''{timedelta_to_vtt_format(start_delta)} --> {timedelta_to_vtt_format(end_delta)}
{body}'''

			out.append(line)  # print(line)

		output = f'''WEBVTT

{'\n\n'.join(out)}
'''
		# print(output)
		with open(f'{rootdir}/liveChatSubs/{post_id}.vtt', 'w', encoding='utf-8') as file:
			file.write(output)


# if len(data) > 1:  # 	break


# with open()

main()
