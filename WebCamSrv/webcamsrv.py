import tornado.ioloop
import tornado.web
import cv2
import os

# Чтение переменных окружения или установка значений по умолчанию
camera_index = int(os.getenv('CAMERA_INDEX', '0'))  # Индекс камеры
width = int(os.getenv('CAMERA_WIDTH', '1920'))       # Ширина изображения
height = int(os.getenv('CAMERA_HEIGHT', '1080'))     # Высота изображения

# Инициализация камеры
camera = cv2.VideoCapture(camera_index)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Проверка установленного разрешения
actual_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Установлено разрешение: {actual_width}x{actual_height}")

class CameraHandler(tornado.web.RequestHandler):
    def get(self):
        ret, frame = camera.read()
        if not ret:
            self.write("Failed to grab frame from camera.")
            return
        _, buffer = cv2.imencode('.jpg', frame)
        self.set_header('Content-Type', 'image/jpeg')
        self.write(buffer.tobytes())

def make_app():
    return tornado.web.Application([
        (r"/", CameraHandler),
    ])

if __name__ == "__main__":
    try:
        app = make_app()
        app.listen(8888)
        print("Server is running on http://localhost:8888/")
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        # Освобождение ресурсов камеры при закрытии приложения
        if camera.isOpened():
            camera.release()
        print("Camera released.")
