import ffmpeg
import os
import subprocess

vids = [f for f in os.listdir('.') if f.lower().endswith(('.mp4','.mkv','.avi', 'm4v'))]
if len(vids) != 1:
    input(f'ALERT: {len(vids)} videos found. Aborting.')
else:
    f = vids[0]

    # Get Meta data
    probe = ffmpeg.probe(f)
    frames = int(probe['streams'][0]['nb_frames'] or 0) # eats to much RAM
    frames = 5000
    
    stream = ffmpeg.input(f)
    scan=f'thumbnail=n={frames}'

    cover = "_cover.jpg"
    ffmpeg.output(stream, cover, vf=scan, vframes=1).overwrite_output().run(quiet=True)
    subprocess.run(['attrib', '+H', cover], shell=True)
    input("Cover generated.")
