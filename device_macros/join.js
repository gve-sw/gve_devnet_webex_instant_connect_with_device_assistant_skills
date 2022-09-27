import xapi from 'xapi';

function join(uri) {
  xapi.Command.Dial({Number: uri});
}

xapi.Event.UserInterface.Assistant.Notification.on((event) => {
  const { Payload } =  event;
  const jsonPayload = JSON.parse(Payload);
  join(jsonPayload.sip_uri);
});