
##BASE BUILD##
# Use the official PyTorch image with CUDA support
FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime AS base

# Print environment information
RUN echo "**** Installed Python ****" && python --version
RUN echo "**** Installed pip ****" && pip --version
RUN echo "**** Installed PyTorch ****" && python -c "import torch; print('PyTorch %s' % torch.__version__)"

# Install ffmpeg as PyAV depend on this library
RUN apt-get update && apt-get install -y ffmpeg gcc

# Set the working directory in the container
WORKDIR /app

##DEV BUILD##
# Copy the requirements file into the container
# This is a separate build stage so that the dependencies are only installed when the requirements.txt file changes
# This will speed up the build process
# This is useful when you are developing the application and frequently changing the code
# The code changes will not trigger the installation of the dependencies again
FROM base AS dev
COPY src/requirements.txt .
RUN pip install --timeout 60 --no-cache-dir -r requirements.txt
#CMD ["python", "main.py"]
ENTRYPOINT [ "./entrypoint.sh" ]

##PROD BUILD##
FROM dev AS prod
COPY src/ .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
