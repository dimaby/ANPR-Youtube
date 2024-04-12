MacBook Pro Apple M1 Pro FaceTime HD camera 
2.1МП (1920*1080)

5MP POE Vechile IMX 335 / 5MP 2,8-12 мм варифокальный объектив (155 USD)
5МП (2592*1944)

Модуль ИК-камеры OV9732 с USB, автоматическое переключение, видеоплата дневного/ночного видения, 1 МП, регулируемый фокус, 72 градуса (18 USD)
1MP (1280*720)

Модуль камеры Waveshare SC3336 3 Мп (B) с высокой чувствительностью, высоким SNR, низкой производительностью, совместим с серией LuckFox Pico (17 USD)
3MP (2304*1296)

git clone "https://github.com/dimaby/ANPR-Youtube"
cd ANPR-Youtube
git pull --force

Локально:
pip3 install matplotlib pytesseract opencv-python tornado
python3 ~/ANPR-Youtube/WebCamSrv/webcamsrv.py
python3 WebCamSrv/webcamsrv.py --camera_url "rtsp://<user>:<password>@<ip/host>"

Собрать в докер:
sudo chmod 666 /dev/video0
docker build -t webcamsrv ~/ANPR-Youtube/WebCamSrv/.
docker run -p 8888:8888 --device /dev/video0:/dev/video0 -e CAMERA_INDEX=0 -e CAMERA_WIDTH=1280 -e CAMERA_HEIGHT=720 webcamsrv

как сервис
docker run -d --restart always -p 8888:8888 --device /dev/video0:/dev/video0 webcamsrv
docker ps
docker stop <container_id_or_name>
docker rm <container_id_or_name>
