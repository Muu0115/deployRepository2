// bmi_calculator.js（外部ファイル）
function calculateBMI(height) {
    var weight = document.getElementById('weight').value;
    var bmi = weight / ((height / 100) ** 2);
    document.getElementById('bmi').innerText = 'あなたのBMI: ' + bmi.toFixed(2);
}

window.onload = function() {
    var height = parseFloat(document.getElementById('user-height').innerText);
    document.getElementById('weight').addEventListener('input', function() {
        calculateBMI(height);
    });
}
