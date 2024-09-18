#!/bin/bash
nvidia-smi
echo '[Executing] main.py file'
python -c 'import torch; print(f"PyTorch={torch.__version__}; CUDA Supported={torch.cuda.is_available()}; CUDA Device count={torch.cuda.device_count()}");'
python -u main.py --input_dir /input --output_dir /output --model_name $MODEL_NAME --device $DEVICE 
echo '[Done]'