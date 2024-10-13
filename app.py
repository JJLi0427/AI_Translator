from flask import Flask, request, render_template, jsonify
import json
import requests
import logging


logging.basicConfig(level=logging.INFO)

# backend server by fkask
app = Flask(__name__)

PROMPT_1="en指英语,cn指中文,ja指日文,ko指韩语"
PROMPT_2="model_1是将内容翻译到指定语言的模式,model_2是按照场景需求给出对应语言内容的模式."
PROMPT_3="示例: input:我想要一桶炸鸡; from cn to en; model_1"
PROMPT_4="应该回答: I want a bucket of fried chicken."
PROMPT_5="示例: input:我在麦当劳店里想向店员点一桶炸鸡; from cn to en; model_2"
PROMPT_6="应该回答: Hello, I want a bucket of fried chicken."
PROMPT_7="下面是一个获取到的实际数据,给出最终的回答: "
PROMPT_TEXT = f"{PROMPT_1}\n{PROMPT_2} {PROMPT_3}\n{PROMPT_4} {PROMPT_5}\n{PROMPT_6}"

@app.route('/')
def index():
    return render_template('translator.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form['inputText']
    input_lang = request.form['inputLang']
    output_lang = request.form['outputLang']
    trans_model = request.form['transModel']
    
    logging.info(f"Input text:{input_text}, Input language: {input_lang}, Output language: {output_lang}")
    introduction_text = f"###input:{input_text}; from {input_lang} to {output_lang}; {trans_model}"
    # TODO: Add translation logic here
    res = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json = {
            "model": "qwen2:0.5b", 
            "messages": [
                {
                    "role": "system", 
                    "content": PROMPT_TEXT
                },
                {
                    "role": "user", 
                    "content": introduction_text
                }
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
            logging.info(f"Final response: {message}")
            return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)