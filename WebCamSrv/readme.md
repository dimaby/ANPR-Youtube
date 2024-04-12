git clone "https://github.com/dimaby/ANPR-Youtube"
cd ANPR-Youtube
git pull --force

Locally:
pip3 install matplotlib pytesseract opencv-python tornado
python3 ~/ANPR-Youtube/WebCamSrv/webcamsrv.py
python3 WebCamSrv/webcamsrv.py --camera_url "rtsp://<user>:<password>@<ip/host>"

Build in Docker:
sudo chmod 666 /dev/video0
docker build -t webcamsrv ~/ANPR-Youtube/WebCamSrv/.
docker run -p 8888:8888 --device /dev/video0:/dev/video0 -e CAMERA_INDEX=0 -e CAMERA_WIDTH=1280 -e CAMERA_HEIGHT=720 webcamsrv
docker run -p 8888:8888 --device /dev/video0:/dev/video0 -e CAMERA_RTSP_URL="rtsp://<user>:<password>@<ip/host>" webcamsrv

Run as a service:
docker run -d --restart always -p 8888:8888 --device /dev/video0:/dev/video0 webcamsrv
docker ps
docker stop <container_id_or_name>
docker rm <container_id_or_name>


Some cameras parameters:
MacBook Pro Apple M1 Pro FaceTime HD camera
2.1MP (1920*1080)
5MP POE Vechile IMX 335/5MP 2.8-12mm Varifocal Lens (AliExpress 155 USD)
5MP (2592*1944)
OV9732 USB IR Camera Module Auto Switch Day/Night Video Card 1MP Adjustable Focus 72 Degree (AliExpress 18 USD)
1MP (1280*720)
Waveshare SC3336 3MP (B) Camera Module High Sensitivity, High SNR, Low Performance, Compatible with LuckFox Pico Series (AliExpress 17 USD)
3MP (2304*1296)

