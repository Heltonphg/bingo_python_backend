function WebSocketTest() {
  let id = 3;
  ws = new WebSocket(`ws://127.0.0.1:8000/auth/${id}/`);
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
