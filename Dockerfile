FROM python:3.14.0rc3-alpine3.22

# Install build tools
RUN apk add --no-cache \
    build-base \
    python3-dev \
    musl-dev \
    linux-headers \
    libsodium-dev \ 
    ffmpeg \
    opus \
    opus-dev 

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt
RUN pip install audioop-lts 
RUN pip install -U discord.py yt-dlp PyNaCl

COPY . .

CMD ["python", "app.py"]