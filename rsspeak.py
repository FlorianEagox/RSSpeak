import feedparser
from TTS.api import TTS
import re
import os

voice = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
def convert_text_to_speech(text, output_file, clone_sample_path):
	voice.tts_to_file(text, speaker_wav=clone_sample_path, language="en", file_path=output_file)

def main(rss_feed_url, output_folder):
	feed = feedparser.parse(rss_feed_url)
	
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	for entry in feed.entries:
		title = entry.title
		content = entry.content[0].value if 'content' in entry else entry.summary
		# Clean HTML tags if any
		cleaner = re.compile('<[^>]*>')
		content = re.sub(cleaner, '', content)

		# Remove special characters from file name
		title = ''.join(e for e in title if e.isalnum())

		# Convert text to speech
		output_file = os.path.join(output_folder, f"{title}.mp3")
		convert_text_to_speech(content, output_file, "me_talking.wav")
		print(f"Converted '{title}' to speech: {output_file}")

if __name__ == "__main__":
	rss_feed_url = "https://tessapainter.com/feed.xml"
	output_folder = "output"

	main(rss_feed_url, output_folder)