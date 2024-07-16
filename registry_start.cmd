set REGISTRY=C:\registry
mkdir %REGISTRY%
podman rm registry
podman run --privileged -d --name registry -p 5000:5000 -v %REGISTRY%:/var/lib/registry:z --restart=always registry