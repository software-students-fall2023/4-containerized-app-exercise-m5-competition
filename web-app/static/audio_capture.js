let mediaRecorder;
let audioChunks = [];

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the normal submission of the form

    // Display a processing message
    document.getElementById("response-message").innerHTML = "<p class='recording-status'>Processing audio file...</p>";

    let formData = new FormData(this); // 'this' refers to the form

    fetch('/api/upload_audio', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        updateResultPage(data); // Use the same function to update the page
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        document.getElementById("response-message").innerHTML = "<p class='error-status'>Error uploading file, please try again!</p>";
    });
});

document.getElementById("start-recording").addEventListener("click", async () => {
    console.log("Start recording button clicked");
    document.getElementById("start-recording").disabled = true;
    document.getElementById("stop-recording").disabled = false;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    mediaRecorder.start();

    // Update UI to show recording status
    document.getElementById("response-message").innerHTML = "<p class='recording-status'>Recording in progress...</p>";
});

document.getElementById("stop-recording").addEventListener("click", () => {
    console.log("Stop recording button clicked");
    mediaRecorder.stop();
    document.getElementById("stop-recording").disabled = true;
    document.getElementById("start-recording").disabled = false;

    // Update UI to show recording has stopped
    document.getElementById("response-message").innerHTML = "<p class='recording-status'>Recording stopped. Processing audio...</p>";

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        sendAudioToServer(audioBlob);
        console.log("Recording stopped");
    };
});

function sendAudioToServer(audioBlob) {
    console.log("Sending audio to server");
    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.wav");

    fetch("/api/js_upload_audio", {
        method: "POST",
        body: formData
    })
    .then(async response => {
        if (!response.ok) {
            const error_body = await response.json();
            console.log(error_body);
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Upload successful", data);
        updateResultPage(data); 
    })
    .catch(error => {
        console.error("Error uploading audio:", error);
    });
}

function updateResultPage(data) {
    const resultContainer = document.getElementById("response-message");
    let htmlContent = `
        <div>
            <h3>Transcribed Text:</h3>
            <p>${data.transcript}</p>
        </div>
    `;

    // Check if sentiment is -2 and display 'N/A' if true
    if (data.sentiment === -2) {
        htmlContent += `
            <div>
                <h3>Sentiment Polarity:</h3>
                <p>N/A</p>
            </div>
        `;
    } else if (data.sentiment >= -1 && data.sentiment <= 1) {
        htmlContent += `
            <div>
                <h3>Sentiment Polarity:</h3>
                <p>${data.sentiment}</p>
            </div>
        `;
        let sentimentInterpretation = "Sentiment Interpretation: Neutral"; // default
        if (data.sentiment > 0.5) {
            sentimentInterpretation = "Sentiment Interpretation: Strongly Positive";
        } else if (data.sentiment > 0) {
            sentimentInterpretation = "Sentiment Interpretation: Slightly Positive";
        } else if (data.sentiment < -0.5) {
            sentimentInterpretation = "Sentiment Interpretation: Strongly Negative";
        } else if (data.sentiment < 0) {
            sentimentInterpretation = "Sentiment Interpretation: Slightly Negative";
        }
        htmlContent += `<p class="sentiment-interpretation">${sentimentInterpretation}</p>`;
    }

    if (data.filename) { // If the user is logged in
        htmlContent += `
            <div>
                <h3>Listen to the Audio:</h3>
                <audio controls>
                    <source src="${serverUrl}:7001/audio/${data.filename}" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
            </div>
        `;
    }

    resultContainer.innerHTML = htmlContent;
}

document.getElementById('audio-file').addEventListener('change', function() {
    // This code will run when the file input changes
    var fileName = this.files[0].name; // Gets the file name
    document.getElementById('file-chosen').textContent = fileName; // Updates the span text
});
