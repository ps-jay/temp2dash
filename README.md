# temp2wemo
TEMPer USB temperature to control a Wemo to turn on and off a freezer

## Build for ARM (Raspberry Pi Zero):
```
docker build -t local/temp2wemo -f Dockerfile.arm .
```

## Run:
```
docker run \
    --detach \
    --memory 192m \
    --privileged \
    --tty \
    --restart=always \
    --net=host \
    --name=temp2wemo \
    --env MONITOR_UUID=<healthchecks.io token> \
    --env SLEEP_TIME=<e.g. 60> \
    --env TEMP_SENSOR=<e.g. 0, or 1> \
    --env TEMP_SCALE=<e.g. 1, 0.8, etc.> \
    --env TEMP_OFFSET=<e.g. -2, 0, etc.> \
    local/temp2wemo
```

### P. Jay's params
* TEMPer2_M12_V1.3: offset=1; scale=1
* TEMPerV1.4: offset=-9; scale=1
