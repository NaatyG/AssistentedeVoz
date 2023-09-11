from IPython.display import Javascript, Audio, display
from google.colab import output
from base64 import b64decode
import whisper
import openai
from gtts import gTTS


# Código Javascript para reproduzir o áudio
RECORD = """
const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
const b2text = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = e => resolve(e.srcElement.result)
  reader.readAsDataURL(blob)
})
var record = time => new Promise(async resolve => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  recorder = new MediaRecorder(stream)
  chunks = []
  recorder.ondataavailable = e => chunks.push(e.data)
  recorder.start()
  await sleep(time)
  recorder.onstop = async ()=>{
    blob = new Blob(chunks)
    text = await b2text(blob)
    resolve(text)
  }
  recorder.stop()
})
"""

def record(sec=5):
  # Executa o código Javascript para gravar o áudio
    display(Javascript(RECORD))
    js_result = output.eval_js('record(%s)' % (sec * 1000))
    # Decodifica o áudio gravado para formato de áudio
    audio = b64decode(js_result.split(',')[1])
    # Salva o arquivo de áudio gravado
    file_name = 'request_audio.wav'
    with open(file_name,'wb') as f:
        f.write(audio)
    # Carrega o arquivo de áudio gravado
    return Audio(file_name)

# Grava o audio do usuario e salva em um arquivo
print('Gravando...')
record_file = record()

# Exibe o audio gravado
display(Audio(record_file, autoplay=False))

# Selecione o modelo do Whisper que melhor atenda sua necessidade
model = whisper.load_model("small")

# Transcreve o áudio gravado
result = model.transcribe(record_file, fp16=False, language="pt-br")
transcription = result["text"]
print(transcription)

openai.api_key = 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

response = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [ {"role": "user", "content": transcription} ]
)

# Obtém a resposta gerada pelo chatgpt
chatgpt_response = response.choices[0].message.content
print(chatgpt_response)

# Cria um objeto gTTS para gerar o áudio da resposta
gtts_object = gTTS(text=chatgpt_response, lang="pt-br", slow=False)

# Salva o áudio da resposta em um arquivo
response_audio = "response_audio.wav"
gtts_object.save(response_audio)

# Exibe o áudio da resposta
display(Audio(response_audio, autoplay=True))