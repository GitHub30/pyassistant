# PyAssistant
Make your raspberry pi a smart speaker :speaker:

## ABILLITIES

- Acoustic Speech Recognition
    - Cognitive Service Speech Api with sox
- Hotword Detection
    - Snowboy (not implemented yes)
- Speech Language Understanding
    - Cognitive Service LUIS Api
- Text To Speech
    - Open Jtalk
- IR Control
    - lirc (not implemented yet)
- Web Server Control Panel (not implemented yet)

## INSTALL

create virtual environment
```sh
python3 -m venv ~/venv/pyassistant
source ~/venv/pyassistant/bin/activate
```

clone and install package
```sh
git clone https://github.com/garicchi/pyassistant.git
cd pyassistant
pip install -r requirements.txt
```

## RUN ASSISTANT IN CONSOLE

```sh
python app.py
```
