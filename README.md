# ANPR-Youtube

docker build -t noderedopigpio ~/ANPR-Youtube/NodeRedOpiGpio/.
docker build -t webcamsrv ~/ANPR-Youtube/WebCamSrv/.

docker-compose build
docker-compose up -d
docker-compose down
docker-compose restart
