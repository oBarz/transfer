rem running multiple ignite nodes on single container
rem REF: https://ignite.apache.org/docs/latest/installation/installing-using-docker
mkdir conf
mkdir storage1
mkdir storage2

set PORTS=-p 10800:10800 -p 11211:11211 -p 47100:47100 -p 47500:47500 -p 49112:49112
set CONF1=-v %CD%\conf:/conf:z -e CONFIG_URI=/conf/example-ignite.xml -v %CD%\storage1:/storage:z -e IGNITE_WORK_DIR=/storage 
set CONF2=-v %CD%\conf:/conf:z -e CONFIG_URI=/conf/example-ignite.xml -v %CD%\storage2:/storage:z -e IGNITE_WORK_DIR=/storage 
set OPTS=-e JVM_OPTS="-Xms4g -Xmx4g -server -XX:MaxMetaspaceSize=256m -Djava.net.preferIPv4Stack=true"

podman pod kill ignite
podman pod rm ignite
podman pod create --name ignite %PORTS% 
podman run --pod ignite -d --name ignite_1 %CONF1% %OPTS% docker.io/apacheignite/ignite:2.16.0-jdk11
podman run --pod ignite -d --name ignite_2 %CONF2% %OPTS% docker.io/apacheignite/ignite:2.16.0-jdk11

