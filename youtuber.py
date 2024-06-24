###################################################
# YOUTUBER
# Author       : Adeebdanish
# version      : 1.0
# Description  : YouTube video downloader
###################################################

import re
import sys
from pytube import YouTube


class Youtuber:
    aud = False
    path = "downloads"
    progress_bar = True

    @staticmethod
    def _display_progress_bar_(
            bytes_received, filesize, ch: str = "█", scale: float = 0.55
    ):

        columns = 35
        max_width = int(columns * scale)

        filled = int(round(max_width * bytes_received / float(filesize)))
        remaining = max_width - filled
        progress_bar = ch * filled + " " * remaining
        percent = round(100.0 * bytes_received / float(filesize), 1)
        text = f"downloading: |{progress_bar}| {percent}% | {round((bytes_received / 1024) / 1024, 2)} MiB\t\r"
        sys.stdout.write(text)
        sys.stdout.flush()

    def _on_progress_(
            self, stream, chunk, bytes_remaining
    ):

        self.file_size = self.set_res.filesize

        bytes_received = self.file_size - bytes_remaining
        self._display_progress_bar_(
            bytes_received, self.file_size)

    @staticmethod
    def check_url(url: str):

        youtube_pattern = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/")
        youtube_regex = re.compile(youtube_pattern)
        match = youtube_regex.match(url)

        return bool(match)

    def _get_progess_bar_(self):

        if self.progress_bar:
            return self._on_progress_
        return None

    def get_video(self, url: str):

        on_progress_callback = self._get_progess_bar_()
        self.video = YouTube(
            url,
            on_progress_callback=on_progress_callback
        )
        self.streams = self.video.streams

    def get_res(self):

        tags = {}

        filtered_streams = self.streams.filter(
            progressive=True,
        ).order_by('resolution')

        if self.aud:
            tags = {stream.abr: stream.itag for stream in self.streams if stream.type == "audio"}

        else:
            tags = {stream.resolution: stream.itag for stream in filtered_streams if stream.type == "video"}

        return tags

    def get_file_name(self):

        file_name = self.video.title
        pattern = r'[^a-zA-Z0-9\s]'
        file_name = re.sub(pattern, '', file_name)

        return file_name

    def get_title(self):

        return self.video.title

    def download(self, tag):

        self.set_res = self.streams.get_by_itag(tag)
        file_name = self.get_file_name() + "." + self.set_res.subtype
        self.set_res.download(self.path)


def help_text():
    hlp_txt = '''
 Usage : Youtuber.py -u [URL] -r [RESOLUTION] [OPTIONS]

 OPTIONS
-------------------------------------

  -u    : set url
  -aud  : download audio only
  -r    : set download resolution
        : A - Show available resolutions

-------------------------------------

'''
    print(hlp_txt)
