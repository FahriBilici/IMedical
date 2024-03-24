# syntax=docker.io/docker/dockerfile:1
FROM --platform=linux/riscv64 cartesi/python:3.10-slim-jammy as base

LABEL io.sunodo.sdk_version="0.2.0"
LABEL io.cartesi.rollups.ram_size="8Gi"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    busybox-static=1:1.30.1-7ubuntu3 \
    ca-certificates \
    curl=7.81.0-1ubuntu1.15 \
    build-essential \
    libssl-dev \
    git \
    autoconf \
    automake \
    libtool \
    pkg-config \
    libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Download and compile CMake, this step is cached until CMAKE_VERSION changes
#ARG CMAKE_VERSION=3.21.0
#RUN curl -LO https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}.tar.gz \
#    && tar -zxvf cmake-${CMAKE_VERSION}.tar.gz \
#    && cd cmake-${CMAKE_VERSION} \
#    && ./bootstrap \
#    && make \
#    && make install

# Copy only the requirements.txt first to cache the pip install step
WORKDIR /opt/cartesi/dapp

COPY cmake /usr/local/bin/cmake

COPY cmake-3.21 /usr/local/share/cmake-3.21

RUN chmod +x /usr/local/bin/cmake

ENV CMAKE_ROOT=/usr/local/share/cmake-3.21

ENV PATH="/usr/local/bin:${PATH}"

COPY ./requirements.txt /opt/cartesi/dapp/

RUN pip install --upgrade pip && \
    pip install --find-links https://prototyp3-dev.github.io/pip-wheels-riscv/wheels/ -r requirements.txt --no-cache-dir

# Copy the rest of the application
#COPY ./mmproj-model-f16.gguf /opt/cartesi/dapp/
#COPY ./ggml-model-q4_k.gguf /opt/cartesi/dapp/
COPY ./dapp.py /opt/cartesi/dapp/

ENV PATH="/opt/cartesi/bin:${PATH}"
ENV ROLLUP_HTTP_SERVER_URL="http://127.0.0.1:5004"

ENTRYPOINT ["rollup-init"]
CMD ["python3", "dapp.py"]
