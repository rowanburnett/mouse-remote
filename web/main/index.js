const socket = io();
let clientPassword;

function startup() {
    setPassword();

    const keyboard = document.getElementById('keyboard-button');
    const textInput = document.getElementById('text-input');
    keyboard.addEventListener('click', () => {
        textInput.focus();
    })
    
    const touchpad = document.getElementById('touchpad');
    touchpad.addEventListener('touchmove', handleMove);
    touchpad.addEventListener('touchstart', handleStart);

    touchpad.addEventListener('click', () => {
        socket.emit('leftClicked', clientPassword)
    })

    touchpad.addEventListener('dblclick', () => {
        socket.emit('doubleClicked', clientPassword)
    })

    textInput.addEventListener('keydown', (evt) => { // doesn't work for characters in chrome??
        if (evt.key === 'Enter') {
            socket.emit('keyPressed', clientPassword, evt.key);
        }
    })

    let startComposition;
    
    textInput.addEventListener('focus', () => {
        startComposition = true;
    })
    
    textInput.addEventListener('input', (evt) => {
        let composition;
        if (evt.inputType === 'deleteContentBackward') {
            socket.emit('keyPressed', clientPassword, 'Backspace');
        if (evt.inputType === 'deleteContentForward') {
            socket.emit('keyPressed', clientPassword, 'Delete');
        }
        } else if (evt.inputType === 'insertCompositionText') { // firefox uses this for autocorrect
            if (startComposition) {
                composition = evt.data;
                socket.emit('keyPressed', clientPassword, composition);
                startComposition = false;
            } else if (evt.data.length > composition.length) {
                composition = evt.data.slice(composition.length - 1);
                socket.emit('keyPressed', clientPassword, composition);
            }
        } else {
            startComposition = true;
            // evt.target.value = '';
            socket.emit('keyPressed', clientPassword, evt.data);
        }
    })

    textInput.addEventListener('focusout', (evt) => {
        evt.target.value = '';
    })

    const leftMouse = document.getElementById('left-mouse')
    leftMouse.addEventListener('click', () => {
        socket.emit('leftClicked', clientPassword)
    })

    const rightMouse = document.getElementById('right-mouse')
    rightMouse.addEventListener('click', () => {
        socket.emit('rightClicked', clientPassword)
    })

    const form = document.getElementById('form')
    form.addEventListener('submit', (evt) => {
        evt.preventDefault();
        let password = evt.currentTarget.password.value;
        document.cookie = `password=${password}; max-age=${60*60*24*365}; Secure`
        setPassword();
        evt.currentTarget.password.value = '';
    })
}

function setPassword() {
    try {
        clientPassword = document.cookie
            .split('; ')
            .find((row) => row.startsWith('password='))
            ?.split('=')[1];
    } catch(err) {
        console.log(err); 
    }
}

function handleStart(evt) {
    socket.emit('touchStarted', clientPassword);
}

function handleMove(evt) {
    evt.preventDefault();

    let touchPoint = evt.touches.item(0);
    let touchX = touchPoint.screenX / screen.width;
    let touchY = touchPoint.screenY / screen.height;

    if (evt.touches.length === 1) {
        socket.emit('mouseMoved', clientPassword, [touchX, touchY]);
    }
    if (evt.touches.length > 1) {
        socket.emit('mouseScrolled', clientPassword, [touchX, touchY]);
    }
}

document.addEventListener('DOMContentLoaded', startup);
