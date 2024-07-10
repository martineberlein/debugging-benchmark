FROM python:3.12

# Install dependencies for pyenv
# RUN apt-get update && apt-get install -y \
#     curl \
#     git \
#     build-essential \
#     libssl-dev \
#     zlib1g-dev \
#     libbz2-dev \
#     libreadline-dev \
#     libsqlite3-dev \
#     wget \
#     llvm \
#     libncurses5-dev \
#     libncursesw5-dev \
#     xz-utils \
#     tk-dev \
#     libffi-dev \
#     liblzma-dev \
#     python3-openssl \
#     libgdbm-dev \
#     libnss3-dev \
#     libedit-dev \
#     libgdbm-compat-dev \
#     && rm -rf /var/lib/apt/lists/*

# Install pyenv
RUN curl https://pyenv.run | bash

# Set environment variables for pyenv
ENV PATH="/root/.pyenv/bin:/root/.pyenv/shims:${PATH}"

# Initialize pyenv in the current shell and bashrc
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    bash -c 'source ~/.bashrc && pyenv init --path && pyenv init -'

# Set the working directory
WORKDIR /app

# Copy the application files
# COPY script.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the command to keep the container running
# CMD ["tail", "-f", "/dev/null"]