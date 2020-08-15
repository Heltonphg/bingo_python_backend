function WebSocketTest() {
  let id = 2;
  ws = new WebSocket(`ws://localhost:8000/auth/${id}/`);
  return ws;
}
function Send() {
 let ws = WebSocketTest();
  ws.onopen = function () {
    ws.send(
      JSON.stringify({
        key: 'anviar.aviso',
        value: {
          message: 'User Connected',
        },
      })
    );
  };
}

WebSocketTest();
