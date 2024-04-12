python3 WebCamSrv/webcamsrv.py  

docker build -t camera-server webcamsrv/.
docker run -p 8888:8888 --device /dev/video0:/dev/video0 -e CAMERA_INDEX=1 -e CAMERA_WIDTH=1280 -e CAMERA_HEIGHT=720 camera-server

MacBook Pro Apple M1 Pro FaceTime HD camera 
2.1МП (1920*1080)

5MP POE Vechile IMX 335 / 5MP 2,8-12 мм варифокальный объектив (155 USD)
5МП (2592*1944)

Модуль ИК-камеры OV9732 с USB, автоматическое переключение, видеоплата дневного/ночного видения, 1 МП, регулируемый фокус, 72 градуса (18 USD)
1MP (1280*720)

Модуль камеры Waveshare SC3336 3 Мп (B) с высокой чувствительностью, высоким SNR, низкой производительностью, совместим с серией LuckFox Pico (17 USD)
3MP (2304*1296)

