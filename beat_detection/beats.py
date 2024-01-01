# These "import statements" let Python know that we're using the "packages"
# named "pytube" and "librosa". Packages are self-contained, reusable pieces of
# Python code that are available for public use. They must be installed on your
# computer first. Instructions are available at https://pypi.org/.

# Pytube is a utility that downloads things from YouTube. This "from A import B"
# syntax means "import only the subcomponent B from the package A"
from pytube import YouTube

# Librosa gives us functions for audio and music analysis
import librosa

# Some utilities we'll use to save and play the results
import soundfile
import os

# ##############################################################################
# STEP 1 - Download some music from YouTube
# ##############################################################################
# Don't worry about streams and all that, the only thing that matters here is
# we plug in a URL and the audio gets saved as "music.mp3". We only download
# if the file isn't already there, so if you change URLs be sure to delete the
# file "music.mp3" so that it gets downloaded again!
if not os.path.exists("./music.mp3"):
    video = YouTube("https://www.youtube.com/watch?v=EAAnlSEVk94")
    audio_stream = video.streams.filter(
        only_audio=True, mime_type="audio/mp4").order_by("abr").desc().first()
    audio_stream.download(filename="music.mp3")

# ##############################################################################
# STEP 2 - Download some music from YouTube
# ##############################################################################

# First, we use librosa to load the audio file we just obtained. The syntax
# "librosa.load(...)" calls a function (subroutine) named "load" in the package
# librosa.

# Unlike Visual Basic, you're not required to declare variables in Python - so
# there's no Python equivalent to "Dim foobar As Integer". The first time you
# assign a value to a variable, it's considered implicitly declared.

# Also unlike Visual Basic, Python allows functions to return multiple values.
# So here we're declaring two new variables named "time_series" and
# "sampling_rate" and assigning them the values returned by the load function.
# More info about what those represent is available at
# https://librosa.org/doc/latest/glossary.html
time_series, sampling_rate = librosa.load("music.mp3")

# beat_track estimates the beat, returning the tempo and an array in which
# each entry represents the time at which a beat occurred
tempo, beats = librosa.beat.beat_track(y=time_series, sr=sampling_rate)

# clicks takes an array representing a series of beats (from above) and
# generates a click track with clicks on those beats
click_track = librosa.clicks(
    frames=beats, sr=sampling_rate, length=len(time_series))

# Librosa makes the plus operator work the way we'd like it to - adding a
# time series to another time series (the time series of our original audio to
# the time series of the click track we just made) gives the time series of
# the combined audio
time_series_with_clicks = time_series + click_track

# We take the time series of the audio with the click track, save it to
# "music_with_clicks.mp3" and open it
soundfile.write("music_with_clicks.mp3", time_series_with_clicks,
                format="mp3", samplerate=sampling_rate)
os.startfile("music_with_clicks.mp3")
