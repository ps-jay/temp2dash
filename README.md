# temp2dash
TEMPer USB temperature to Dashing dashboard

## Build for ARM (Raspberry Pi):
```
docker build -t local/temp2dash -f Dockerfile.arm .
```

## Build for x86 (everything else!):
```
docker build -t local/temp2dash -f Dockerfile.x86 .
``` 

## Run:
```
docker run \
    --detach \
    --memory 128m \
    --privileged \
    --restart=always \
    --name=temp2dash \
    --link dashing:dashing \
    --env DASHING_URL=http://dashing:3030/widgets/<id> \
    --env DASHING_TOKEN=<the_auth_token> \
    --env SLEEP_TIME=<e.g. 60> \
    --env TEMP_SENSOR=<e.g. 0, or 1> \
    --env TEMP_SCALE=<e.g. 1, 0.8, etc.> \
    --env TEMP_OFFSET=<e.g. -2, 0, etc.> \
    local/temp2dash
```

Note: `--link` is optional depending on the URL / network configuration

### P. Jay's params
* TEMPer2_M12_V1.3: offset=-3; scale=1
* TEMPerV1.4: offset=-6.5; scale=1
