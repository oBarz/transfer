set JAVA_HOME=C:\Java\coretto11.0.15_9_64
call gradlew.bat clean assemble jib
set POD=ignite
set CONTAINER=phoenix_client
set CLIENT_IMAGE=localhost:5000/com.clarifi.phoenix/phoenix_client:latest
set CONF=-v %CD%\conf:/conf:z -e CONFIG_URI=/conf/example-ignite.xml 
podman rm %CONTAINER%
podman pull %CLIENT_IMAGE%
podman run -d --pod %POD% --name %CONTAINER% %CONF% %CLIENT_IMAGE%
