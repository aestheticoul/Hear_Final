// Initialize Firebase
var config = {
        apiKey: "AIzaSyDnmQFMztgoIYwuOLoOWUIIb8zpKZxs2eM",
        authDomain: "contactform-c6a0c.firebaseapp.com",
        databaseURL: "https://contactform-c6a0c-default-rtdb.firebaseio.com",
        projectId: "contactform-c6a0c",
        storageBucket: "contactform-c6a0c.appspot.com",
        messagingSenderId: "644611779374",
        appId: "1:644611779374:web:b6e6b1210497ca8ef3e8bf"
    
    
};
firebase.initializeApp(config);

//Reference messages collection
let messagesRef = firebase.database().ref('messages');

//listen to form
document.getElementById('contactForm').addEventListener('submit', submitForm);

function submitForm(e){
    e.preventDefault();

    // get Values
    let first_name = getInputVal('name');
    let last_name= getInputVal('company');
    let email = getInputVal('email');
    let phone = getInputVal('phone');
    let message = getInputVal('message');

    //save message

    saveMessage(first_name, last_name, email, phone, message);

    //show alert
    document.querySelector('.alert').style.display='block';

    //Hide alert after 3 s
    setTimeout(function(){
        document.querySelector('.alert').style.display='none';
    }, 3000)
    //clear form
    document.getElementById('contactForm').reset();
}
//function to get form values

function getInputVal(id){
    return document.getElementById(id).value;
}

//save message to firebase
function saveMessage(first_name, last_name, email, phone, message){
    let newMessageRef = messagesRef.push();
    newMessageRef.set({
       first_name: first_name,
        last_name: last_name,
        email: email,
        phone: phone,
        message: message
    })
}