# temp2dash
TEMPer USB temperature to Dashing dashboard

Setup: 

```
docker build --tag="local/temp2dash" .
docker run -d -m 96m \
    --privileged \
    --link dashing:dashing \
    --name=temp2dash local/temp2dash
```

Cronjob:

```
# inside temp
* * * * * root docker start -a temp2dash 2> /dev/null
```
