rem running multiple ignite nodes on single container
rem REF: https://ignite.apache.org/docs/latest/installation/installing-using-docker
mkdir conf
mkdir storage1
mkdir storage2

PORTS='-p 8080:8080 -p 5005:5005 -p 10800:10800 -p 11211:11211 -p 47100:47100 -p 47500:47500 -p 49112:49112'
CONF1='-v ./conf:/conf:z -e CONFIG_URI=/conf/example-ignite.xml -v ./storage1:/storage:z -e IGNITE_WORK_DIR=/storage'
CONF2='-v ./conf:/conf:z -e CONFIG_URI=/conf/example-ignite.xml -v ./storage2:/storage:z -e IGNITE_WORK_DIR=/storage'
OPTS=''

podman pod kill ignite
podman pod rm ignite
podman pod create --name ignite $PORTS
podman run --pod ignite -d --name ignite_1 $CONF1 $OPTS docker.io/apacheignite/ignite:2.16.0-jdk11
podman run --pod ignite -d --name ignite_2 $CONF2 $OPTS docker.io/apacheignite/ignite:2.16.0-jdk11

