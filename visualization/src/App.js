import React, { useState, useEffect } from "react";
import logo from "./logo.svg";
import "./App.css";
import app from "firebase/app";
import "firebase/database";
import "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyAx5QHALVtmfATVLiSTB_wnmRqc1cjjdac",
  authDomain: "detritech-fd3cd.firebaseapp.com",
  databaseURL: "https://detritech-fd3cd.firebaseio.com",
  projectId: "detritech-fd3cd",
  storageBucket: "detritech-fd3cd.appspot.com",
  messagingSenderId: "626100418454",
  appId: "1:626100418454:web:af56d895c4c5d6901e0fb7"
};

class Firebase {
  constructor() {
    app.initializeApp(firebaseConfig);

    this.storage = app.storage();
    this.db = app.database();
  }

  getImage = () => {};

  getStatus = () => {};
}

function Image({ url, imageKind }) {
  return (
    <>
      {url ? (
        <div>
          <p>{imageKind}</p>
          <img src={url} width="400" height="400" />
        </div>
      ) : (
        <p style={{ width: "400px", height: "400px", textAlign: "center" }}>
          Waiting for {imageKind}
        </p>
      )}
    </>
  );
}

var firebase = new Firebase();

function App() {
  const [status, setStatus] = useState("TAKE_IMAGE");
  const [originalImage, setOriginalImage] = useState(null);
  const [croppedImage, setCroppedImage] = useState(null);
  const [modelResult, setModelResult] = useState(null);

  var statusRef = firebase.db.ref("message");
  var storageRef = firebase.storage.ref();

  useEffect(() => {
    statusRef.on("value", function(snapshot) {
      console.log("newStatus : ", snapshot.val());
      setStatus(oldStatus => snapshot.val());
    });
  }, []);

  useEffect(() => {
    if (status === "IMAGE_UPLOADED") {
      storageRef
        .child("images/mountains.jpg")
        .getDownloadURL()
        .then(url => setOriginalImage(url));
    }

    if (status === "IMAGE_TREATED") {
      storageRef
        .child("images/cropped_image.png")
        .getDownloadURL()
        .then(url => setCroppedImage(url));
      storageRef
        .child("images/result.png")
        .getDownloadURL()
        .then(url => setModelResult(url));
    }
  }, [status]);

  return (
    <div className="App">
      <header className="App-header">
        Status: {status}
        <div className="imgs">
          {/* {originalImage ? (
            <img src={originalImage} width="400" height="400" />
          ) : (
            "Waiting for image"
          )}
          {croppedImage && <img src={croppedImage} width="400" height="400" />}
          {modelResult && <img src={modelResult} width="400" height="400" />} */}
          <Image url={originalImage} imageKind="original image" />
          <Image url={croppedImage} imageKind="cropped image" />
          <Image url={modelResult} imageKind="result image" />
        </div>
      </header>
    </div>
  );
}

export default App;
