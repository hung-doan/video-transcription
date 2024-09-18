# RUNBOOK
## Run 
### Directly from image
```powershell
$inpur_dir = "E:/ML-Data/video-transcription/input"
$output_dir = "E:/ML-Data/video-transcription/output"
$model_name = "base"
$device = "cuda"
docker run --gpus=all -i -t --env MODEL_NAME=${model_name} --env DEVICE=${device} -v ${inpur_dir}:/input -v ${output_dir}:/output hungdoan/video-transciption:latest 
```


### Using docker-compose

Using `base` model
```
docker compose -p "video-transcript" --env-file .env --env-file .env.base up --build --remove-orphans
```

Using `largev3` model
```
docker compose -p "video-transcript" --env-file .env --env-file .env.largev3 up --build --remove-orphans
```


## Build
### Dev
```
docker buildx build --progress=plain --target dev .
```

#### Prod

Local build
```
docker buildx build --progress=plain --tag hungdoan/video-transciption:latest --target prod .
```

Push to Docker's registry
```
docker buildx build --target prod --tag hungdoan/video-transciption:latest --output=type=registry .
```

