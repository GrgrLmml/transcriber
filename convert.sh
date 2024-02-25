
#ffmpeg -i $1 -f segment -segment_time 300 -acodec libmp3lame -reset_timestamps 1 output%03d.mp3

ffmpeg -i $1 -acodec libmp3lame audio.mp3
insanely-fast-whisper --file-name audio.mp3 --device-id mps --batch-size 4 --hf_token $2
python3 src/convert.py --output-file $1.txt



#rm audio.mp3

