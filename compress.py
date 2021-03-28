#got rid of the ugly keyboard interrupt and changed it for something better looking 
#removed making the user to run commands for audio and video
#added import signal for keyboard interrupt

import os
import ffmpeg
import math
import time
from pymediainfo import MediaInfo
import signal

def keyboardInterruptHandler(signal, frame):
    print(" ")
    print(" ")
    print("Compresor closing...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

print("8MB File Compressor for Discord (and others)")
video = input("Please input your video file name. It should be located in the same directory as this script: ")
audio_kbps = input("What audio length would you like to have in the output? (Default: 96kbps): ")
if audio_kbps == "":
    audio_kbps = 96
user_os = input("What's your OS? Input " + "w " + "for Windows and " + "l " + "for Linux. (w/l): ")
file_size = input("What output file size would you like? (in megabytes) (default: 8): ")
if file_size == "":
    file_size = 8
print("")
print("*** Please, read the following info ***")
print("You can choose what codec to encode the video in now.")
print("Recommended: VP9. To use it, you can just click your Enter key, it will set the codec as VP9")
print("You could also choose H264, though, it's not recommended.")
print("You can choose H265 too, but Discord won't be able to play it.")
print("AV1 is the best codec right now, but, Discord can't play it either.")
print("")
print("Available options: 1 for VP9, 2 for H264, 3 for H265, 4 for AV1.")
codec = input("What codec would you like? (default: VP9): ")
if codec == "":
    codec = "libvpx-vp9"
if codec == "1":
    codec = "libvpx-vp9"
if codec == "2":
    codec = "libx264"
if codec == "3":
    codec = "libx265"
if codec == "4":
    codec = "libaom-av1"
print("You will be prompted to choose the video compression preset. Recommended: veryslow. You can choose medium too, fast compression, worse quality. Placebo is not needed, it dosen't vary from veryslow that much.")
preset = input("What video preset would you like? (Options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo): ")
if preset != "ultrafast" or preset != "superfast" or preset != "veryfast" or preset != "faster" or preset != "fast" or preset != "medium" or preset != "slow" or preset != "slower" or preset != "veryslow" or preset != "placebo":
    print("You prompted nothing / something that is not in the list. Preset will set as veryslow as default.")
    preset = "veryslow"


media_info = MediaInfo.parse(video)

duration_in_ms = media_info.tracks[0].duration
video_length = duration_in_ms / 1000
video_length = round(video_length)
video_length = video_length - 1


bitrate = int(file_size) * 8192 / video_length
bitrate = round(bitrate)
bitrate = bitrate - audio_kbps

# Starting to encode

if user_os == "w":
    print(" ")
    print("Compressing video and audio...") #added
    print("")
    windows1 = "ffmpeg -y -i " + video + " -c:v " + codec + " -b:v " + str(bitrate) + "k -preset " + preset + " -pass 1 -an -f null nul && " + r"/"
    windows2 = "ffmpeg -i " + video + " -c:v " + codec + " -b:v " + str(bitrate) + "k -preset " + preset + " -pass 2 -c:a aac -b:a " + str(audio_kbps) + "k output.mp4"
    os.system(windows1)
    os.system(windows2)
    print("")
    print("")
    print("You should now have a file called output.mp4 in this directory.")
    print("Files with the extension .log or .mbtree can be safely deleted in this directory.")
    exit()
else:
    # "/" is an escape path if you do r"/" it will be a literal character instead of a path
    print(" ")
    print("Compressing video and audio...") #added
    print("")
    linux1 = "./ffmpeg -y -i " + video + " -c:v " + codec + " -b:v " + str(bitrate) + "k -preset " + preset + " -pass 1 -an -f null /dev/null && " + r"/"
    linux2 = "./ffmpeg -i " + video + " -c:v " + codec + " -b:v " + str(bitrate) + "k -preset " + preset + " -pass 2 -c:a aac -b:a " + str(audio_kbps) + "k output.mp4"
    os.system(linux1)
    os.system(linux2)
    print("")
    print("")
    print("You should now have a file called output.mp4 in this directory.")
    print("Files with the extension .log or .mbtree can be safely deleted in this directory.")
    exit()
