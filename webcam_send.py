import cv2
import time
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher

from messages import imagen_pb2 as video_frame_pb2

ecal_core.initialize("Python Video Publisher")

pub = ProtoPublisher("video_stream", video_frame_pb2.VideoFrame)

cap = cv2.VideoCapture(0)
counter = 0
msg = video_frame_pb2.VideoFrame()
while ecal_core.ok():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam", frame)

    # Codificar a JPEG
    quality = 80
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        continue

    h, w = frame.shape[:2]


    msg.frame_data = buf.tobytes()
    msg.width = w
    msg.height = h
    msg.channels = frame.shape[2] if frame.ndim == 3 else 1
    msg.encoding = video_frame_pb2.JPEG
    msg.frame_number = counter
    msg.timestamp = time.time()
    msg.compression_quality = quality
    msg.is_keyframe = True

    pub.send(msg)
    counter += 1

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
ecal_core.finalize()