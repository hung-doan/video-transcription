# Use the official PyTorch image with CUDA support
FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime

# Print environment information
RUN echo "**** Installed Python ****" && python --version
RUN echo "**** Installed pip ****" && pip --version
RUN echo "**** Installed PyTorch ****" && python -c "import torch; print('PyTorch %s' % torch.__version__)"
#RUN echo "**** Installed CUDA ****" && nvcc --version
#RUN echo "**** Installed cuDNN ****" && cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2

# Install ffmpeg as PyAV depend on this library
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install the dependencies
RUN pip install --timeout 60 --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ .

# Command to run the application
CMD ["python", "main.py"]