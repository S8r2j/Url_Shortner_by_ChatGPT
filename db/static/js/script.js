document.getElementById('urlForm').onsubmit = function(event) {
    event.preventDefault();

    var url = document.getElementById('urlInput').value;
    fetch("http://127.0.0.1:5000/shorten/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "url=" + encodeURIComponent(url)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('shortenedURL').textContent = data.shortened_url;
        document.getElementById('resultBox').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
    });
};
