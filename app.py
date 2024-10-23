from flask import Flask, request, render_template, jsonify
import json
import requests
import argparse

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, help="Model you want to use", default="qwen2:0.5b")
args = parser.parse_args()
app.config['TRANSLATION_MODEL'] = args.model

PROMPT_1 = "en英语,cn中文,ja日文,ko韩语"
PROMPT_2 = "model_1直接翻译到指定语言,model_2按情境给出恰当翻译."
PROMPT_3 = "例如: input:我要一桶炸鸡; from cn to en; model_1, 应该回答: I want a bucket of fried chicken."
PROMPT_4 = "例如: input:我在麦当劳店里想向店员点一桶炸鸡; from cn to en; model_2, 应改回答: Hello, I want a bucket of fried chicken."
PROMPT_5 = "以下是实际数据: "
PROMPT_TEXT = f"{PROMPT_1}\n{PROMPT_2}\n{PROMPT_3}\n{PROMPT_4}\n{PROMPT_5}"

@app.route('/')
def index():
    return render_template('translator.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form['inputText']
    input_lang = request.form['inputLang']
    output_lang = request.form['outputLang']
    trans_model = request.form['transModel']
    model = app.config['TRANSLATION_MODEL']
    print(f"###Input text: {input_text}, Input language: {input_lang}, Output language: {output_lang}")
    introduction_text = f"input:{input_text}; from {input_lang} to {output_lang}; {trans_model}, 给出最终的回答："
    
    res = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": PROMPT_TEXT},
                {"role": "user", "content": introduction_text}
            ],
            "stream": True
        },
    )
    res.raise_for_status()

    output = ""
    for line in res.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content

        if body.get("done", False):
            message["content"] = output
            print(f"###Final response: {message}")
            return jsonify(message)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
