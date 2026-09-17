import sys
import time
import os


import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import mi_mensaje_pb2 as mi_mensaje_pb2

ecal_core.initialize("Python Protobuf Subscriber")

sub = ProtoSubscriber("mensaje 1",
                     mi_mensaje_pb2.HelloWorld)
protobuf_message = mi_mensaje_pb2.HelloWorld()
counter = 0

while ecal_core.ok():
    isReceived, protobuf_message, _ = sub.receive(100)
    if isReceived:
        print("name: ",protobuf_message.name)
        print("id: ", protobuf_message.id)
        print("msg: ", protobuf_message.msg)
        print("state: ", protobuf_message.state)



ecal_core.finalize()