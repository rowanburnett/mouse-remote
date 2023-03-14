const socket = io();
let clientPassword;

function startup() {
    setPassword();

    const touchpad = document.getElementById('touchpad');
    touchpad.addEventListener('touchmove', handleMove);
    touchpad.addEventListener('touchstart', handleStart);

    touchpad.addEventListener('click', () => {
        socket.emit('leftClicked', clientPassword)
    })

    touchpad.addEventListener('dblclick', () => {
        socket.emit('doubleClicked', clientPassword)
    })

    const keyboardButton = document.getElementById('keyboard-button')
    const textInput = document.getElementById('text-input');
    keyboardButton.addEventListener('click', () => {
        textInput.focus();
    })

    textInput.addEventListener('input', (evt) => {
        socket.emit('keyPressed', clientPassword, evt.target.value);
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