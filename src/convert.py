import json

import datetime
import argparse


def seconds_to_hhmmssxxx(seconds):
    # Ensure the input is a float to include milliseconds
    seconds = float(seconds)

    # Convert seconds to a timedelta object
    time_delta = datetime.timedelta(seconds=seconds)

    # Extract hours, minutes, seconds, and milliseconds
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((time_delta.microseconds // 1000) / 10)

    # Format the time string
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}"

    return time_str


def run(output_file):
    data = json.load(open('output.json'))
    lines = []
    spk = ''
    line = ''
    nxt_time = 120
    incr = 120
    for idx in range(len(data['speakers'])):
        speaker = data['speakers'][idx]['speaker']
        if speaker != spk:
            spk = speaker
            lines.append(line)
            line = spk + ': '

        ts = data['speakers'][idx]['timestamp'][0]
        if ts > nxt_time:
            nxt_time += incr
            fr = seconds_to_hhmmssxxx(ts)
            line += f"[{fr}] "
        line += data['speakers'][idx]['text'] + ' '

    lines.append(line)

    with open(f'{output_file}', 'w') as f:
        for idx, line in enumerate(lines):
            f.write(f"{line}\n")


def run_text_time(output_file, time_interval=120):
    data = json.load(open('output.json'))
    output = []
    current_time_block = None
    for item in data['speakers']:
        start_time, _ = item['timestamp']
        time_stamp = f"[{int(start_time // 3600):02d}:{int((start_time % 3600) // 60):02d}:{int(start_time % 60):02d}]"
        if current_time_block is None or start_time - current_time_block >= time_interval:
            current_time_block = start_time - (start_time % time_interval)
            output.append(f"{time_stamp}\n\t{item['text'].strip()}")
        else:
            output.append(f"\t{item['text'].strip()}")
    with open(f'{output_file}', 'w') as f:
        for idx, line in enumerate(output):
            f.write(f"{line}\n")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an input JSON file.')
    parser.add_argument('--output-file', type=str, help='Output JSON file path', required=True)

    args = parser.parse_args()

    run_text_time(args.output_file)
