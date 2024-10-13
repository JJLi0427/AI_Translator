document.getElementById('confirmBtn').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
    document.querySelector('.container').style.display = 'flex';
    document.querySelector('.tip').style.display = 'flex';
    document.querySelector('.tip').style.opacity = '1';
});

document.getElementById('translateBtn').addEventListener('click', function(event) {
    event.preventDefault();
    
    const inputText = document.getElementById('inputText').value;
    const inputLang = document.getElementById('inputLang').value;
    const outputLang = document.getElementById('outputLang').value;
    const transModel = document.getElementById('transModel').value;
    
    // 显示加载动画
    document.getElementById('loading').style.display = 'block';
    
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            inputText: inputText,
            inputLang: inputLang,
            outputLang: outputLang,
            transModel: transModel
        })
    })
    .then(response => response.json())
    .then(data => {
        const translatedText = data.content;
        document.getElementById('outputText').value = translatedText;
        
        // 隐藏加载动画
        document.getElementById('loading').style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        
        // 隐藏加载动画
        document.getElementById('loading').style.display = 'none';
    });
});