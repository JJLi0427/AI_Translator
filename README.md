# AI_Translator
For Shengteng AI Competition, to build a embedded AI software

1. Artificial intelligence from Qwen:0.5b model, run by ollama.
2. Develop on originpai embedded device.
3. Desigen a multiple model translator, user can input their needs or only translate text.
4. Use Flask frame to handle connection and message between broswer and server。

<img src="image.png" alt="sample" style="width:75%;"/>

## How to run it
1. Install [ollama](https://ollama.com/download) on your system.
2. Download a [LLM](https://ollama.com/library) you need to use and start it.
3. Run application `python app.py --model ${YOUR_MODEL}`
4. Visit <http://127.0.0.1:5000> to use the AI Translator.