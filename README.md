# speaker_backend
this is a basic backend

function list:
- [x] login and register
- [x] upload audio
- [x] embedder generation
- [x] none model filter
- [x] speech to text
- [x] download result

todo list:

- [x] flask-restful backend basic structure
- [ ] documents
- [x] file upload api
- [x] file download api
- [ ] docker

tips:

- 1. create virtual environment

create venv: `python -m venv ./venv`

activate venv: `.\venv\Scripts\activate`

if u meet error: `CategoryInfo          : SecurityError: (:) []，PSSecurityException`

pls run `powershell.exe -ExecutionPolicy RemoteSigned`

- 2. install dependency

pip install -r requirements.txt

#### attention: pls check your CUDA version to install suitable [pytorch](https://pytorch.org/get-started/previous-versions/), we only test on torch 1.7.0-1.9.0

- 3. create data folder ,database and download model

run folder_creation.sh

run sqlcmd.sh

download deepspeech [model](https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm) and [scorer](https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer), put them into checkpoint/deepspeeech/

download voicefilter [checkpoint](https://github.com/Xumj82/voicefilter/releases/download/chkpoint/chkpt_190000.pt) and [embedder](https://github.com/Xumj82/voicefilter/blob/main/datasets/embedder.pt), put them into checkpoint/voicefilter/

- 4. create table inside database

`python sqliteModel.py`

- 5. start server

`python main.py`
- 6. check if it works
  the api use case is available via the [postman link](https://www.getpostman.com/collections/8953bbf2a1ba81572a9c)