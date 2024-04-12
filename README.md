# ANPR-Youtube

Step7 -- Docker-compose (https://github.com/docker/compose/releases)
sudo curl -L "https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version

docker build -t noderedopigpio ~/ANPR-Youtube/NodeRedOpiGpio/.
docker build -t webcamsrv ~/ANPR-Youtube/WebCamSrv/.

docker-compose build
docker-compose up -d
docker-compose down
docker-compose restart
