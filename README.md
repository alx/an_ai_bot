# Mastodon Bot using DeepDetect prediction services

Replay to follower toots using service predictions from DeepDetect server

![Example](https://raw.githubusercontent.com/alx/an_ai_bot/master/docs/screenshot.png)

https://mastodon.tetaneutral.net/@ai_bot/102363212818441068

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
