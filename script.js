document.getElementById('confirmBtn').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
    document.querySelector('.container').style.display = 'flex';
    document.querySelector('.tip').style.display = 'flex';
    document.querySelector('.tip').style.opacity = '1';
});