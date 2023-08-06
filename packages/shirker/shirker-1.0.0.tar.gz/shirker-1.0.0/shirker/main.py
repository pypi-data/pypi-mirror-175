import argparse
import json
import os
import subprocess
import sys
import traceback

import fsspec
import urllib3


def get_ap():
    a = argparse.ArgumentParser()
    a.add_argument(
        'tokenpath',
        type=str,
        help="path to file containing slack authentication token"
    )
    a.add_argument(
        'channels',
        type=str,
        help="comma seperated channel ids/names to send in"
    )
    a.add_argument(
        "--initial-comment",
        type=str,
        help="optional comment in first message",
        default="Running something important"
    )
    
    return a


def create_send(token, channels, filetype="txt", httppool=None):
    token = token.strip()
    thread_ts = [(channel, None) for channel in channels]
    
    if httppool is None:
        httppool = urllib3.PoolManager()
        
    headers = urllib3.make_headers(
        user_agent=(
            'Mozilla/5.0'
            ' (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6)'
            ' Gecko/20070725 Firefox/2.0.0.6'
        )
    )
    
    def send(initial_comment, filename, file):
        for i, (channel, tts) in enumerate(thread_ts):
            params = {
                "token": token,
                "file": (filename, file),
                "channels": channel,
                "filename": filename,
                "filetype": filetype,
                "initial_comment": initial_comment,
            }

            if tts is not None:
                params['thread_ts'] = tts

            response = httppool.request(
                'POST',
                "https://slack.com/api/files.upload",
                params,
                headers
            )
            if response.status != 200:
                raise IOError("file upload failed")
            
            if tts is None:
                j = json.loads(response.data.decode())
                tts = (
                    list(list(j['file']['shares'].values())[0].values())
                    [0][0]['ts']
                )
                thread_ts[i] = channel, tts
    return send


def run(initial_comment, command, send):
    send(initial_comment, "command", json.dumps(command))
    
    try:
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        err = ''.join(traceback.format_exception(None, e, e.__traceback__))
        send(f"failed to start subprocess", "stderr", err)
        return 1
    
    stdout, stderr = p.communicate()

    for f, b in [(sys.stdout, stdout), (sys.stderr, stderr)]:
        with os.fdopen(f.fileno(), "wb", closefd=False) as fd:
            fd.write(b)
            fd.flush()
    
    if stdout and not stderr:
        send(f"no stderr\nexit code: {p.returncode}", "stdout", stdout)
    elif not stdout and stderr:
        send(f"no stdout\nexit code: {p.returncode}", "stderr", stderr)
    elif not stdout and not stderr:
        send(
            f"no stdout\nno stderr\nexit code: {p.returncode}",
            "nothing",
            b'\n'
        )
    else:
        send(f"exit code: {p.returncode}", "stdout", stdout)
        send(f"", "stderr", stderr)
        
    return p.returncode


def shirker(token, channels, initial_comment, command):
    send = create_send(token, channels)
    return run(initial_comment, command, send)


def main():
    ap = get_ap()
    argv = sys.argv
    
    try:
        c = argv.index("--")
        args = ap.parse_args(argv[1:c])
        command = argv[c + 1:]
    except ValueError:
        print("command to run must follow '--'", file=sys.stderr)
        sys.exit(1)

    token = fsspec.open(args.tokenpath).open().read()
    channels = [c.strip() for c in args.channels.split(",")]
    
    ret = shirker(token, channels, args.initial_comment, command)

    sys.exit(ret)
    

if __name__ == "__main__":
    main()

