const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/html/index.html');
});

io.on('connection', (socket) => {
  socket.on('mouseClicked', () => {
    io.emit('mouse_clicked')
  })
  socket.on('doubleClicked', () => {
    io.emit('double_clicked');
  })
  socket.on('touchStarted', () => {
    io.emit('touch_started')
  })
  socket.on('mouseMoved', (data) => {
    io.emit('mouse_moved', data);
  })
  socket.on('mouseScrolled', (data) => {
   io.emit('mouse_scrolled', data);
 })
})

server.listen(3000, '0.0.0.0', (err) => {
  if (err) {
    console.log(err);
  }
  console.log('listening on *:3000');
});
