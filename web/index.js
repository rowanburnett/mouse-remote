const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/main/index.html');
});

io.on('connection', (socket) => {
  socket.on('password', (password) => {
    socket.join(password);
  })

  socket.on('mouseClicked', (id) => {
    console.log(id)
    io.to(id).emit('mouse_clicked');
  })
  socket.on('doubleClicked', (id) => {
    io.to(id).emit('double_clicked');
  })
  socket.on('touchStarted', (id) => {
    io.to(id).emit('touch_started');
  })
  socket.on('mouseMoved', (id, data) => {
    io.to(id).emit('mouse_moved', data);
  })
  socket.on('mouseScrolled', (id, data) => {
   io.to(id).emit('mouse_scrolled', data);
 })
})

  if (err) {
    console.log(err);
  }
});
