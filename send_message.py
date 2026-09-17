import sys
import time
import os


import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messages import mi_mensaje_pb2 as mi_mensaje_pb2

ecal_core.initialize("Python Protobuf Publisher")

pub = ProtoPublisher("mensaje 1",
                     mi_mensaje_pb2.HelloWorld)
protobuf_message = mi_mensaje_pb2.HelloWorld()
counter = 0

while ecal_core.ok():
    protobuf_message.name = "fulano menganillo"
    protobuf_message.id = counter
    protobuf_message.msg = -123.456
    protobuf_message.state = True
    pub.send(protobuf_message)
    time.sleep(1)
    counter = counter + 1

ecal_core.finalize()