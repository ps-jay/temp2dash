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
    --tty \
    --restart=always \
    --name=temp2dash \
    --env DASHING_URL=http://<host>:3030/widgets/<id> \
    --env DASHING_TOKEN=<the_auth_token> \
    --env SLEEP_TIME=<e.g. 60> \
    --env TEMP_SCALE=<e.g. 1, 0.8, etc.> \
    --env TEMP_OFFSET=<e.g. -2, 0, etc.> \
    local/temp2dash
```
