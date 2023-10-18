const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);

app.use(express.static('main'))

app.get('/', (req, res) => {
  res.sendFile(__dirname + 'index.html');
});

io.on('connection', (socket) => {
  socket.on('password', (password) => {
    socket.join(password);
  })

  socket.on('leftClicked', (id) => {
    io.to(id).emit('left_clicked');
  })
  socket.on('rightClicked', (id) => {
    io.to(id).emit('right_clicked');
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
  socket.on('keyPressed', (id, key) => {
    io.to(id).emit('key_pressed', key);
  })
  socket.on('heartbeat', () => {
    console.log('heartbeat received');
  })
})

server.listen(process.env.PORT, (err) => {
  if (err) {
    console.log(err);
  }
  console.log('listening on ' + process.env.PORT);
});

// server.listen(5000, (err) => {
//   if (err) {
//     console.log(err);
//   }
//   console.log('listening on ' + 5000);
// });
