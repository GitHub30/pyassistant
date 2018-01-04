import subprocess
import re
import pprint


def list_device():
    command = 'aplay -l'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    stdout = p.stdout.read().decode('utf-8')
    stderr = p.stderr.read().decode('utf-8')

    speaker_list = []
    for o in stdout.split('\n'):
        matcher = re.compile(r'.*\d:.*,.*\d:.*')
        r = matcher.match(o)
        if r:

            col = o.split(',')
            card_col = col[0]
            device_col = col[1]
            matcher = re.compile('\d:')
            card_id = matcher.findall(card_col)[0].rstrip(':')

            matcher = re.compile('\[.*\]')
            card_name = matcher.findall(card_col)[0].lstrip('[').rstrip(']')

            matcher = re.compile('\d:')
            device_id = matcher.findall(device_col)[0].rstrip(':')

            matcher = re.compile('\[.*\]')
            device_name = matcher.findall(device_col)[0].lstrip('[').rstrip(']')

            speaker_list.append({
                'card_id':card_id,
                'card_name':card_name,
                'device_id':device_id,
                'device_name':device_name
            })

    command = 'arecord -l'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = p.stdout.read().decode('utf-8')
    stderr = p.stderr.read().decode('utf-8')

    mic_list = []
    for o in stdout.split('\n'):
        matcher = re.compile(r'.*\d:.*,.*\d:.*')
        r = matcher.match(o)
        if r:
            col = o.split(',')
            card_col = col[0]
            device_col = col[1]
            matcher = re.compile('\d:')
            card_id = matcher.findall(card_col)[0].rstrip(':')

            matcher = re.compile('\[.*\]')
            card_name = matcher.findall(card_col)[0].lstrip('[').rstrip(']')

            matcher = re.compile('\d:')
            device_id = matcher.findall(device_col)[0].rstrip(':')

            matcher = re.compile('\[.*\]')
            device_name = matcher.findall(device_col)[0].lstrip('[').rstrip(']')

            mic_list.append({
                'card_id': card_id,
                'card_name': card_name,
                'device_id': device_id,
                'device_name': device_name
            })

    return (mic_list,speaker_list)


def get_default():
    mic_list,speaker_list = list_device()

    command = 'aplay -L'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = p.stdout.read().decode('utf-8')
    stderr = p.stderr.read().decode('utf-8')

    default_card_name = None
    default_device_name = None
    isOn = False
    for o in stdout.split('\n'):
        if o.startswith('sysdefault:CARD'):
            isOn = True
            continue
        if isOn and o.count(':CARD')>0:
            isOn=False
            continue
        if isOn:
            col = o.split(',')
            default_card_name = col[0].lstrip(' ')
            default_device_name = col[1].lstrip(' ')
            break

    default_speaker = None
    for d in speaker_list:
        if d['card_name'] == default_card_name and d['device_name']== default_device_name:
            default_speaker = d

    command = 'arecord -L'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = p.stdout.read().decode('utf-8')
    stderr = p.stderr.read().decode('utf-8')

    default_card_name = None
    default_device_name = None
    isOn = False
    for o in stdout.split('\n'):
        if o.startswith('sysdefault:CARD'):
            isOn = True
            continue
        if isOn and o.count(':CARD') > 0:
            isOn = False
            continue
        if isOn:
            col = o.split(',')
            default_card_name = col[0].lstrip(' ')
            default_device_name = col[1].lstrip(' ')
            break

    default_mic = None
    for d in mic_list:
        if d['card_name'] == default_card_name and d['device_name'] == default_device_name:
            default_mic = d

    return default_mic,default_speaker

if __name__ == '__main__':
    mic,speaker = get_default()
    pprint.pprint(mic)
    pprint.pprint(speaker)