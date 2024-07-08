import React, { useState, useEffect, useRef } from 'react';

function App() {
    const [transcription, setTranscription] = useState('');
    const [websocket, setWebsocket] = useState(null);
    const [isRecording, setIsRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const audioChunksRef = useRef([]);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws/transcription/');
        ws.onopen = () => console.log('Connected to the WebSocket');
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setTranscription(data.transcription);
        };
        ws.onclose = (event) => {
            if (event.wasClean) {
                console.log(`Closed cleanly, code=${event.code}, reason=${event.reason}`);
            } else {
                console.log('Connection died');
            }
        };
        ws.onerror = (error) => {
            console.log(`Error ${error.message}`);
        };
        setWebsocket(ws);
        return () => ws.close();
    }, []);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const newMediaRecorder = new MediaRecorder(stream);
        newMediaRecorder.ondataavailable = (event) => {
            audioChunksRef.current.push(event.data);
        };
        newMediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunksRef.current);
            // We will convert this blob to base64, but you might prefer a different  approach
            const reader = new FileReader();
            console.log(reader)
            reader.onloadend = () => {
                if (websocket) {
                    websocket.send(JSON.stringify({ type: 'audio', audio: reader.result }));
                }
            };
            reader.readAsDataURL(audioBlob);
        };
        newMediaRecorder.start();
        setIsRecording(true);
        setMediaRecorder(newMediaRecorder);
    };

    useEffect(() => {
      return () => {
          if (websocket) {
              websocket.close();
          }
      };
  }, [websocket]);

    const stopRecording = () => {
        if (mediaRecorder) {
            mediaRecorder.stop();
            setIsRecording(false);
        }
    };

    return (
        <div className="App">
            <button onClick={startRecording}>Start Recording</button>
            <button onClick={stopRecording}>Stop Recording</button>
            <textarea value={transcription} readOnly />
        </div>
    );
}

export default App;
