from flask import Flask, request, render_template, jsonify
import logging
from openai import OpenAI
import instructor


logging.basicConfig(level=logging.INFO)

# backend server by fkask
app = Flask(__name__)
# chatbot server by ollama
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="NA",  # required, but unused
    ),
    mode = instructor.Mode.JSON,
)
PROMPT_1="en指英语,cn指中文,ja指日文,ko指韩语"
PROMPT_2="你是会理解用户语义的翻译官,如果用户输入有翻译需求的场景,你会理解并做出合适的翻译"
PROMPT_3="例如你收到: input_text:我在美国的麦当劳想向店员点一桶炸鸡, form cn to en; 这个是用户有场景翻译的需求,你可以这样子回答: I want a bucket of fried chicken."
PROMPT_4="如果你理解到用户只是输入需要翻译的普通的一句话或单词,你也可以正确翻译到指定的语言."
PROMPT_5="例如你收到: input_text:我想要一桶炸鸡, form cn to en; 这个就是指定语言的翻译需求,你可以回答: I want a bucket of fried chicken."
PROMPT_TEXT = f"{PROMPT_1}\n{PROMPT_2}\n{PROMPT_3}\n{PROMPT_4}\n{PROMPT_5}"

@app.route('/')
def index():
    return render_template('translator.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form['inputText']
    input_lang = request.form['inputLang']
    output_lang = request.form['outputLang']
    
    logging.info(f"Input text: {input_text}, Input language: {input_lang}, Output language: {output_lang}")
    introduction_text = f"input_text: {input_text}, from {input_lang} to {output_lang}"
    # TODO: Add translation logic here
    resp = client.chat.completions.create(
        model = "qwen2:0.5b",
        messages=[
            {"role": "system", "content": PROMPT_TEXT},
            {"role": "user", "content": introduction_text}
        ],
        max_retries = 3
    )
    logging.info(f"Model response: {resp}")
    return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True)