document.addEventListener('DOMContentLoaded', function () {
    // DOM이 로드된 후에 실행될 코드
    document.getElementById('submitButton').addEventListener('click', function() {
        sendData();
        console.log("test");
        window.location.href = '/complete'; 
    });
});

function sendData() {
    // 입력한 아이디 가져오기
    var userId = document.getElementById('user_id').value;

    // fetch 함수를 사용하여 플라스크 서버에 데이터 전송
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'user_id': userId }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        // 서버에서 전송한 메시지를 처리하거나 화면에 표시할 수 있습니다.
    })
    .catch(error => {
        console.error('오류 발생:', error);
    });
}
