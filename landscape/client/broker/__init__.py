"""The broker mediates communication between client and server.

Each communication between client and server is initiated by the broker and
performed with an HTTP POST, called `exchange`. The client sends messages
to the server by including them in the request body, and the server sends
messages to the client by including them in the request response (see
L{landscape.broker.exchange} and L{landscape.broker.transport}).

Client components running in different processes (like the manager and the
monitor) connect to the broker process using Unix sockets and can then ask
the broker to perform actions like queuing messages for delivery to the server
or to dispatching them all messages of a given type that the broker receives
from the server (see L{landscape.broker.server} and L{landscape.broker.amp}).

When the broker is started for the first time, it will perform a few exchanges
to register the client against the server using the values provided in the
configuration file (see L{landscape.broker.registration}). If the registration
is successful, or the client was previously registered, the broker will start
pinging the server to check if there are messages that the server wants to
deliver to the client and if so will schedule a urgent exchange (see
L{landscape.broker.ping}). In case the ping check says that there are no
messages from the server, the broker will still perform an exchange every 15
minutes (see L{BrokerConfiguration}), to deliver to the server possible
messages generated by the client (i.e. by the broker itself or by the other
client components like the monitor and the manager).

"""