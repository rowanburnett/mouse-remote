
  const socket = io('http://localhost:5000');
  
  socket.on('clientId', (id) => {
    document.cookie = `password=${id}`
  })
  
  function startup() {
    const box = document.getElementById('box');
    box.addEventListener('touchmove', handleMove);
    box.addEventListener('touchstart', handleStart);
    box.addEventListener('click', (evt) => {
      socket.emit('mouseClicked', clientId)
    })
    box.addEventListener('dblclick', (evt) => {
      socket.emit('doubleClicked', clientId)
    })

    const form = document.getElementById('form')
    form.addEventListener("submit", (evt) => {
        // evt.preventDefault();
        const formData = new FormData(form);
        console.log(formData)
    })
  }
  
  document.addEventListener('DOMContentLoaded', startup);
  
  function handleStart(evt) {
    socket.emit('touchStarted', clientId)
  }
  
  function handleMove(evt) {
    evt.preventDefault();
  
    let touchPoint = evt.touches.item(0);
    let touchX = touchPoint.screenX / screen.width;
    let touchY = touchPoint.screenY / screen.height;
  
    if (evt.touches.length === 1) {
      socket.emit('mouseMoved', clientId, [touchX, touchY]);
    }
    if (evt.touches.length > 1) {
      socket.emit('mouseScrolled', clientId, [touchX, touchY]);
    }
  }    