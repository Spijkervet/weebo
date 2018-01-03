function formToJSON(form) {
  return form.serializeArray().reduce(function(obj, item) {
    obj[item.name] = item.value;
    return obj;
  }, {});
}


var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    socket.emit('connected', {data: 'Still connected'});
});

socket.on('pong', function() {
    // socket.emit('ping', {data: 'Still connected'});
});


socket.on('update', function(data) {
    update(JSON.parse(data));
});


function update(data) {
    $("#version").text(data.version);
    $("#time").text(data.time);
}

$("#consoleForm").submit(function(event) {
    formData = formToJSON($(this));
    formData.button = $(document.activeElement).attr('name');
    console.log(formData);
    socket.emit('consoleMessage', {message: formData.query, api:formData.api, button: formData.button});
    event.preventDefault();
});
