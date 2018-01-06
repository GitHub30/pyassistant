import subprocess
import re
import os


def list_device():
    command = 'aplay -l'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    stdout = p.stdout.read().decode('utf-8')

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

def set_default(mic_card_id,mic_device_id,speaker_card_id,speaker_device_id):
    home = os.environ['HOME']
    asoundrc = os.path.join(home,'.asoundrc')

    template = """
    pcm.!default {
      type asym
       playback.pcm {
         type plug
         slave.pcm "hw:%d,%d"
       }
       capture.pcm {
         type plug
         slave.pcm "hw:%d,%d"
       }
    }
    """%(speaker_card_id,speaker_device_id,mic_card_id,mic_device_id)

    with open(asoundrc,'w') as f:
        f.write(template)


def get_mixer_controls(card_id):
    command = 'amixer -c %d scontrols'%(card_id)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = p.stdout.read().decode('utf-8')
    controls = []
    for o in stdout.split('\n'):
        if o.count("'") > 0:
            cols = o.split("'")
            controls.append(cols[1])
    return controls

def get_current_volume_list(card_id):
    controls = get_mixer_controls(card_id)
    results = {}
    for control in controls:
        command = 'amixer -c %d get %s' % (card_id,control)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = p.stdout.read().decode('utf-8')
        control_volumes = {}
        pattern = r".*: .*\[\d*%\].*"

        for o in stdout.split('\n'):
            if re.search(pattern,o):

                channel = re.search(r".*: ",o).group().lstrip(' ').rstrip(' ').rstrip(':')
                m = re.compile(r"\[\d*%\]")
                volume = m.search(o).group().lstrip('[').rstrip(']').rstrip('%')
                control_volumes[channel]={
                    'volume':int(volume)
                }
        if len(control_volumes)>0:
            results[control] = control_volumes

    return results

def get_current_volume(card_id):
    volumes = get_current_volume_list(card_id)
    volume = None
    for k in volumes.keys():
        control = volumes[k]
        for k2 in control.keys():
            volume = control[k2]['volume']
        break

    return volume


def set_current_volume(card_id,volume):
    controls = get_mixer_controls(card_id)
    for control in controls:
        command = 'amixer -c %s set %s %d' % (card_id, control,volume)
        command += '%'
        subprocess.check_call(command.split(' '))


def use_output_line():
    command = 'amixer cset numid=3 1'
    subprocess.call(command.split(' '))

def use_output_hdmi():
    command = 'amixer cset numid=3 2'
    subprocess.call(command.split(' '))

def get_output_line():
    command = 'amixer contents'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = p.stdout.read().decode('utf-8')

    is_three = False
    value = None
    for o in stdout.split('\n'):
        if o.count('numid=3,') > 0:
            is_three=True
            continue
        if o.count('  : values=')>0 and is_three:
            value = int(o.replace('  : values=',''))
            break

    line = None
    if value == 1:
        line = 'LINE'
    elif value == 2:
        line = 'HDMI'
    return line

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_output_line())
