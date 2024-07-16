Main Classes
------------

1. PersistentNode - runs Ignite server node with persistent storage enabled.
   -Xms512m -Xmx512m recommended

2. HelloWorld - runs Ignite client node with basic connectivity tests

3. LoadSampleTimeSeriesData - creates fake time series data, settings are hard-coded im main() method

======================

This is a demo for Ignite cluster dev environment with Podman containerization.
To be used on Windows.
Prerequisites:
1. enable Windows fearures via "turn Windows features on or off":
* Virtual Machine Support
* Windows Subsystem for Linux
2. install podman desktop [https://podman-desktop.io/downloads], which will install, initialize and run podman.
3. configure local registry for insecure connection

IMPORTANT: IT DOES NOT WORK FOR WSL2!!! at least I cannot get it to work on WSL2
  Per documentation published all over the web, you need to create
  file: C:\Users\<USERNAME>\.config\containers\registries.conf.d\myregistry.conf
  content:
  [[registry]]
  location="localhost:5000"
  insecure=true

  it does not work with latest podman 4.4.4; I tried a few hours, so do not spend your time trying.

WHAT YOU NEED IS: use linux way. 
  good thing is -- that will also work on our future AWS linux hosts.
  your goal is to update a config file located in \\wsl.localhost\podman-machine-default\etc\containers\registries.conf.d\ folder
  on my system that file is 999-podman-machine.conf

  steps to make preparation for unsecure registry:
  a) run command from host windows shell, [if on linux -- skip this step]
       podman machine ssh
     this command opens ssh session to WSL2 linux host running inside
  b) you might want to have some decent text editor on linux [if nano editor is available-- skip this step]
     check https://phoenixnap.com/kb/use-nano-text-editor-commands-linux
     I successfully installed nano on WSL2 with
       sudo yum install nano
  c) navigate to /etc/containers/registries.conf.d
       cd /etc/containers/registries.conf.d
  d) edit conf file, in my case 999-podman-machine.conf
       sudo nano 999-podman-machine.conf
     add lines below to that file
       [[registry]]
       location="localhost:5000"
       insecure=true

  e) use CTRL-O to write updated file to disk, then CRTL-X to exit from editor

  for the sake of sanity I restarted the WSL2 virtual machine:
    podman machine stop
    podman machine start

==================================

Build `hello world` app and run it in podman container 
1. Run `registry_start.cmd` 
* it starts local image registry on port 5000
2. Run `cluster_in_a_pod.cmd`
* it starts two Ignite nodes inside of a Podman's pod -- these will be running in linux environments 
2. Run `rebuild.cmd` 
* it rebuilds Java code
* creates jar file with the code
* packages it into image on top of openjdk 11 temurine
* pushes it to local image registry as localhost:5000/com.clarifi.phoenix/phoenix_client
* cleans up previously existed container [if any]
* refreshes localhost:5000/com.clarifi.phoenix/phoenix_client in podman
* request podman to run local image localhost:5000/com.clarifi.phoenix/phoenix_client
  * that will execute the Ignite client com.clarifi.phoenix.ashes.node.HelloWorld
  * which in turn will send remote task to be executed on Ignite cluster running in Podman