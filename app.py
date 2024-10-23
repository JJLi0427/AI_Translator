from flask import Flask, request, render_template, jsonify
import json
import requests
import argparse

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, help="Model you want to use", default="llama3:8b")
args = parser.parse_args()
app.config['TRANSLATION_MODEL'] = args.model

PROMPT_1 = "本次对话中我希望你可以翻译一些语句。我们设置以下键值对:en英语,zh中文,ja日文,ko韩语"
PROMPT_2 = "action_1直接翻译到指定语言,action_2按情境给出更有创造性的翻译."
PROMPT_3 = "例如: input:我要一桶炸鸡; from cn to en; action_1, 应该回答: I want a bucket of fried chicken."
PROMPT_4 = "例如: input:我在麦当劳店里想向店员点一桶炸鸡; from cn to en; action_2, 应改回答: Hello, I want a bucket of fried chicken."
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
    introduction_text = f"input:{input_text}; from {input_lang} to {output_lang}; {trans_model}, 给出只含翻译结果的回答："  
    
    try:  
        res = requests.post(  
            "http://192.168.0.108:11434/api/chat",
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
            if line:  # 确保行不为空
                body = json.loads(line)  
                if "error" in body:  
                    raise Exception(body["error"])  
                if body.get("done") is False:  
                    message = body.get("message", {})  
                    content = message.get("content", "")  
                    output += content  # 拼接所有返回内容
        
        return jsonify({"content": output})  # 返回完整拼接的内容

    except requests.exceptions.RequestException as e:  
        return jsonify({"error": str(e)}), 500  # 如果请求失败，返回错误信息


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
