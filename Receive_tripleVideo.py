import numpy as np
import cv2
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber

from messages import trinocular_pb2

ecal_core.initialize("Python Trinocular Subscriber")

sub = ProtoSubscriber("trinocular_stream", trinocular_pb2.TripleVideoFrame)


def decode_frame(msg_frame, label):
    buf = np.frombuffer(msg_frame.frame_data, dtype=np.uint8)
    frame = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if frame is None:
        return None
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1.0, (0, 255, 0), 2, cv2.LINE_AA)
    return frame


while ecal_core.ok():
    isReceived, msg, _ = sub.receive(100)
    if isReceived:
        left = decode_frame(msg.left, "LEFT")
        center = decode_frame(msg.center, "CENTER")
        right = decode_frame(msg.right, "RIGHT")

        if left is None or center is None or right is None:
            continue

        cv2.imshow("Left RX", left)
        cv2.imshow("Center RX", center)
        cv2.imshow("Right RX", right)

        if cv2.waitKey(1) == 27:  # ESC
            break

cv2.destroyAllWindows()
ecal_core.finalize()