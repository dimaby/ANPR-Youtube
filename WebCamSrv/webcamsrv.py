import tornado.ioloop
import tornado.web
import cv2
import os
import argparse

class Camera:
    def __init__(self, camera_index, camera_url, width, height):
        self.camera_index = camera_index
        self.camera_url = camera_url
        self.width = width
        self.height = height
        self.connect()

    def connect(self):
        if self.camera_url:
            print(f"Initializing RTSP camera with URL: {self.camera_url}")
            self.camera = cv2.VideoCapture(self.camera_url)
        else:
            print(f"Initializing local camera with index: {self.camera_index}")
            self.camera = cv2.VideoCapture(self.camera_index)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        try:
            # Attempt to set timeout if supported
            self.camera.set(cv2.CAP_PROP_READTIMEOUT_MS, 5000)
        except AttributeError:
            print("Warning: Timeout setting not supported")

        actual_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f"Resolution: {actual_width}x{actual_height}")

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Failed to grab frame from camera, attempting to reconnect...")
            self.camera.release()
            self.connect()
            ret, frame = self.camera.read()
        return ret, frame

    def release(self):
        if self.camera.isOpened():
            self.camera.release()

class CameraHandler(tornado.web.RequestHandler):
    def initialize(self, camera):
        self.camera = camera

    def get(self):
        ret, frame = self.camera.get_frame()
        if not ret:
            self.write("Failed to grab frame from camera.")
            return
        _, buffer = cv2.imencode('.jpg', frame)
        self.set_header('Content-Type', 'image/jpeg')
        self.write(buffer.tobytes())

def make_app(camera):
    return tornado.web.Application([
        (r"/", CameraHandler, {'camera': camera}),
    ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebCam Server Configuration")
    parser.add_argument('--camera_index', type=int, default=None, help='Index of the webcam device')
    parser.add_argument('--camera_url', type=str, default=None, help='RTSP URL of the remote camera')
    parser.add_argument('--width', type=int, default=None, help='Width of the camera resolution')
    parser.add_argument('--height', type=int, default=None, help='Height of the camera resolution')

    args = parser.parse_args()

    camera_index = args.camera_index if args.camera_index is not None else int(os.getenv('CAMERA_INDEX', '0'))
    camera_url = args.camera_url if args.camera_url is not None else os.getenv('CAMERA_RTSP_URL', '')
    width = args.width if args.width is not None else int(os.getenv('CAMERA_WIDTH', '1920'))
    height = args.height if args.height is not None else int(os.getenv('CAMERA_HEIGHT', '1080'))

    camera = Camera(camera_index, camera_url, width, height)

    try:
        app = make_app(camera)
        app.listen(8088)
        print("Server is running on http://localhost:8088/")
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        camera.release()
        print("Camera released.")
