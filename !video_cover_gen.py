import ffmpeg
import os
import subprocess

vids = [f for f in os.listdir('.') if f.lower().endswith(('.mp4','.mkv','.avi', 'm4v', 'wmv'))]
if len(vids) != 1:
    input(f'ALERT: {len(vids)} videos found. Aborting.')
else:
    f = vids[0]

    # Get Meta data
    probe = ffmpeg.probe(f)
    # frames = int(probe['streams'][0]['nb_frames'] or 0) # eats to much RAM, also not supported by wmv
    frames = 5000
    
    stream = ffmpeg.input(f)
    stream = ffmpeg.filter(stream, 'thumbnail', n=frames)
    stream = ffmpeg.filter(stream, 'scale', 'iw*sar', 'ih')
    stream = ffmpeg.filter(stream, 'setsar', '1')

    cover = "_cover.jpg"
    cover_tmp = "_cover_%03d.jpg"
    try:
        ffmpeg.output(stream, cover_tmp, vframes=1).overwrite_output().run(
            capture_stdout=True,
            capture_stderr=True
        )
    except ffmpeg.Error as e:
        print("FFMPEG STDERR:")
        print(e.stderr.decode('utf8', errors='ignore'))
        input("Press Enter to exit...")

    os.replace("_cover_001.jpg", cover)
    subprocess.run(['attrib', '+H', cover], shell=True)
    input("Cover generated.")
