from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('translator.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form['inputText']
    input_lang = request.form['inputLang']
    output_lang = request.form['outputLang']
    
    # 在这里添加翻译逻辑
    translated_text = f"Translated {input_text} from {input_lang} to {output_lang}"
    
    return translated_text

if __name__ == '__main__':
    app.run(debug=True)