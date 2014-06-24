from django_socketio import events
"""
@events.on_message(channel="my channel")
def message(request, socket, context, message):
    my_message = message + "which is mishaka"
    print(my_message)
    socket.send({'mymessage':my_message})
    """