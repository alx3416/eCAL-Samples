import cv2
import time
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher

from messages import trinocular_pb2
from messages import imagen_pb2 as video_frame_pb2

ecal_core.initialize("Python Trinocular Publisher")

pub = ProtoPublisher("trinocular_stream", trinocular_pb2.TripleVideoFrame)

# Abrir las 3 cámaras (ajusta los índices según tu sistema)
caps = [cv2.VideoCapture(0), cv2.VideoCapture(1), cv2.VideoCapture(2)]

counter = 0
quality = 80


def fill_frame(msg_frame, frame, counter, quality):
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        return False

    h, w = frame.shape[:2]
    msg_frame.frame_data = buf.tobytes()
    msg_frame.width = w
    msg_frame.height = h
    msg_frame.channels = frame.shape[2] if frame.ndim == 3 else 1
    msg_frame.encoding = video_frame_pb2.JPEG
    msg_frame.frame_number = counter
    msg_frame.timestamp = time.time()
    msg_frame.compression_quality = quality
    msg_frame.is_keyframe = True
    return True


msg = trinocular_pb2.TripleVideoFrame()

while ecal_core.ok():
    frames = []
    all_ok = True
    for cap in caps:
        ret, frame = cap.read()
        if not ret:
            all_ok = False
            break
        frames.append(frame)

    if not all_ok:
        break

    # Mostrar cada stream
    cv2.imshow("Left", frames[0])
    cv2.imshow("Center", frames[1])
    cv2.imshow("Right", frames[2])

    # Llenar los 3 sub-mensajes
    if not fill_frame(msg.left, frames[0], counter, quality):
        continue
    if not fill_frame(msg.center, frames[1], counter, quality):
        continue
    if not fill_frame(msg.right, frames[2], counter, quality):
        continue

    pub.send(msg)
    counter += 1

    if cv2.waitKey(1) == 27:  # ESC
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()
ecal_core.finalize()