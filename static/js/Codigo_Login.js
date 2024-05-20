$(function() {
    $(".btn").click(function() {
        $(".form-signin").toggleClass("form-signin-left");
        $(".form-signup").toggleClass("form-signup-left");
        $(".frame").toggleClass("frame-long");
        $(".signup-inactive").toggleClass("signup-active");
        $(".signin-active").toggleClass("signin-inactive");
        $(".forgot").toggleClass("forgot-left");   
        $(this).removeClass("idle").addClass("active");
    });
});

$(function() {
    $(".btn-signup").click(function() {
        $(".nav").toggleClass("nav-up");
        $(".form-signup-left").toggleClass("form-signup-down");
        $(".success").toggleClass("success-left"); 
        $(".frame").toggleClass("frame-short");
    });
});

$(function() {
    $(".btn-signin").click(function() {
        $(".btn-animate").toggleClass("btn-animate-grow");
        $(".welcome").toggleClass("welcome-left");
        $(".cover-photo").toggleClass("cover-photo-down");
        $(".frame").toggleClass("frame-short");
        $(".profile-photo").toggleClass("profile-photo-down");
        $(".btn-goback").toggleClass("btn-goback-up");
        $(".forgot").toggleClass("forgot-fade");
    });
});

// Configuración de Firebase
const firebaseConfig = {
    apiKey: "AIzaSyCdgESi9SAXpml0VApEMt4nEQnA-C3Oabk",
    authDomain: "eventos-deportivos-961d9.firebaseapp.com",
    databaseURL: "https://eventos-deportivos-961d9-default-rtdb.firebaseio.com",
    projectId: "eventos-deportivos-961d9",
    storageBucket: "eventos-deportivos-961d9.appspot.com",
    messagingSenderId: "271914301823",
    appId: "1:271914301823:web:aae5c55d9b314174a1824a",
    measurementId: "G-HHNYS2083K"
  };

// Inicializar Firebase
firebase.initializeApp(firebaseConfig);

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    firebase.auth().signInWithEmailAndPassword(email, password)
        .then((userCredential) => {
            userCredential.user.getIdToken().then((idToken) => {
                fetch('/auth/verifyToken', { // Asegúrate de que esta URL sea correcta
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({token: idToken})
                })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/home'; // O la URL a la que quieres redirigir
                    } else {
                        throw new Error('Failed to authenticate');
                    }
                })
                .catch((error) => {
                    console.error('Authentication failed:', error);
                });
            });
        })
        .catch((error) => {
            console.error("Authentication failed:", error.message);
        });
});
