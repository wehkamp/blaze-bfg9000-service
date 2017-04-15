# blaze-bfg9000-service
Just something fun to inject in your container platform to randomly kill containers!

This container expects to be deployed to a Mesos/Marathon-based containerplatform where it will sit in the background, waiting, luring at containers...
Per interval it will wake up and start shooting at whatever services (tasks) are running. Only containers that are in a healhty state and with a sane uptime can be shot.

While shooting, ammo is limited. Out of ammo means the round has passed.

This thing is about resiliency testing your container service platform (hint: _chaos monkey_).

### power-ups
Unlocked only by chance, there are two power-ups available.

>QUAD DAMAGE

> This doubles the frags, killing not 1 but 2 containers of the same service

> AMMO

>  Gives more ammo, so more containers can (and will) be destroyed

### configuration
Configurable items, may be set as environment variable:

| Name             | Description                   |
|:-----------------|:------------------------------|
| `SERVICE_PORT`          | HTTP service port (availble for health checks) |
| `MARATHON_HOST`         | fqdn to Marathon HTTP API, no protocol/port required |
| `MIN_CONTAINERS`        | number of _godmode_ containers per application (can't be killed) |
| `MIN_LIFETIME_SECS`     | containers must be this old before they become a valid target |
| `RUNTIME_INTERVAL_SECS` | run every _this_ interval |
| `AMMO`                  | amount of bullets in clip |

## usage
```
docker build -f Dockerfile.in -t ${USER_ORG}/blaze-bfg9000-service .
docker push ${USER_ORG}/blaze-bfg9000-service
```

And deploy the resulting container to your platform.
