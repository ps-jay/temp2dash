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
    --env DASHING_URL=http://dashing:3030/widgets/inside \
    --env SLEEP_TIME=60 \
    --env TEMP_SENSOR=0 \
    --env TEMP_SCALE=1 \
    --env TEMP_OFFSET=0 \
    local/temp2dash
```

Note: `--link` is optional depending on the URL / network configuration
