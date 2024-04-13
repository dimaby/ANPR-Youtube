import tornado.ioloop
import tornado.web
import cv2
import os
import argparse
import time
import pytesseract
import numpy as np

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
        print(f"Resolution set to: {actual_width}x{actual_height}")

    def get_frame(self):
        ret, frame = self.camera.read()
        if not ret:
            print("Failed to grab frame from camera, attempting to reconnect...")
            self.camera.release()
            self.connect()
            ret, frame = self.camera.read()
        return frame

    def release(self):
        if self.camera.isOpened():
            self.camera.release()

class CameraHandler(tornado.web.RequestHandler):
    def initialize(self, camera, carplate_haar_cascade):
        self.camera = camera
        self.carplate_haar_cascade = carplate_haar_cascade

    def get(self):
        start_time = time.time()
        detect = self.get_argument('detect', None)
        crop = self.get_argument('crop', None)
        ocr = self.get_argument('ocr', None)
        frame = self.camera.get_frame()
        
        if frame is None:
            self.write("Failed to grab frame from camera.")
            return

        if detect == '1':
            frame, carplate_img = self.detect_carplate(frame, crop == '1')

            if crop == '1' and carplate_img is not None:
                frame = self.resize_keep_aspect_ratio(carplate_img, 640, 480)
                if ocr == '1':
                    self.perform_ocr(carplate_img) 

        process_time = time.time() - start_time
        print(f"Frame processing: {process_time:.2f} seconds")

        _, buffer = cv2.imencode('.jpg', frame)
        self.set_header('Content-Type', 'image/jpeg')
        self.write(buffer.tobytes())

    def resize_keep_aspect_ratio(self, carplate_img, target_width, target_height):
        h, w = carplate_img.shape[:2]
        scale = min(target_width / w, target_height / h)
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized_img = cv2.resize(carplate_img, (new_w, new_h))

        return resized_img

    def detect_carplate(self, image, crop):
        carplate_rects = self.carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
        carplate_img = None
        for x, y, w, h in carplate_rects:
            if crop:
                carplate_img = image[y:y+h, x:x+w]
                return image, carplate_img
            else:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw red rectangle
        return image, carplate_img
    
    def perform_ocr(self, carplate_img):
        carplate_extract_img_gray = cv2.cvtColor(carplate_img, cv2.COLOR_RGB2GRAY)
        ocr_result = pytesseract.image_to_string(
            carplate_extract_img_gray,
            config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
        print('Detected Plate Number:', ocr_result.strip())

def make_app(camera, carplate_haar_cascade):
    return tornado.web.Application([
        (r"/", CameraHandler, {'camera': camera, 'carplate_haar_cascade': carplate_haar_cascade}),
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

    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, 'models', 'haarcascade_russian_plate_number.xml')
    print("Loading Haar Cascade from:", model_path)
    carplate_haar_cascade = cv2.CascadeClassifier(model_path)

    camera = Camera(camera_index, camera_url, width, height)

    try:
        app = make_app(camera, carplate_haar_cascade)
        app.listen(8088)
        print("Server is running on http://localhost:8088/")
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        camera.release()
        print("Camera released.")
