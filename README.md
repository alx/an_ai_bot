# Ananas AI Bot with DeepDetect

Replay to follower toots using service predictions from DeepDetect server

## Requirements

- https://github.com/chr-1x/ananas
- https://deepdetect.com

## Run

```
cp config.cfg.sample config.cfg
nano config.cfg # change access token, client id and client secret
ananas config.cfg
```

## Issues

- TypeError: 'module' object is not callable : https://github.com/chr-1x/ananas/issues/18
