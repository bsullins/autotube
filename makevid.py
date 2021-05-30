from moviepy.editor import *
from pathlib import Path
import datetime
import click


# create list of clips
def read_clip_data(clip_data, video_end_timecode):
    first_clip = "00:00:00"
    last_clip = None

    clip_list = []

    lines = clip_data.split("\n")
    for line in lines:
        if line.startswith("START"):
            pass
        elif line.startswith("STOP"):
            pass
        elif len(line) == 0:
            pass
        else:
            if last_clip is None:
                last_clip = first_clip

            clip_list.append([last_clip, line])
            last_clip = line

    clip_list.append([last_clip, video_end_timecode])

    return clip_list

# define transition
def add_transitions(vid):
    t1 = vfx.fadein(clip=vid, duration=0.25)
    t2 = vfx.fadeout(clip=t1, duration=0.25)
    return t2

# get input from user
@click.command()
@click.option('-m', help='Movie file to splice')
@click.option('-c', help='Text file from OBS InfoWriter with clip times')

# make video
# Ned to modify to combine clips with transition using text file
# Current design is to cut a single video into multiple clips
# New design will be to create a single video form multiple clips

def splice_video(m, c):
    # Read the video
    src = VideoFileClip(m)

    # Get it's length
    length = datetime.timedelta(seconds=int(src.duration))
    last_timecode = str(length)

    # Determine clip points
    clip_file = Path(c)
    dt = "-".join(clip_file.stem.split("-")[:-1])
    print("Date is", dt)

    clip_data = clip_file.read_text()
    clips = read_clip_data(clip_data, last_timecode)

    # setup outro
    # create from image
    outro_img = ImageClip("outro-logo.png", duration=9)
    outro_vid = add_transitions(outro_img)

    # create sub-clips
    videos = [src.subclip(clip[0], clip[1]) for clip in clips]

    # add transitions
    clips = [add_transitions(video) for video in videos]

    # add outro
    # highlights = [concatenate_videoclips([clip, outroVid]) for clip in clips]
    highlights = [concatenate_videoclips([clip, outro_vid]) for clip in clips]

    # create output
    for h, highlight in enumerate(highlights):
        highlight.write_videofile(f"output/{dt}-h{h}.mp4", fps=30)


if __name__ == "__main__":
    splice_video()