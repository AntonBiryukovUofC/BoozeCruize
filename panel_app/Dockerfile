FROM python:3

WORKDIR /usr/src/app
RUN mkdir panel_app
WORKDIR /usr/src/app/panel_app

# Install XVFB for headless firefox / selenium
RUN apt update && apt upgrade -y
RUN apt install -y xvfb firefox-esr

# Timezone
ENV TZ America/Edmonton

# Python Requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Xvfb
RUN echo "#!/bin/sh" > /usr/src/app/Xvfb.start
RUN echo "/usr/bin/Xvfb :99 -ac -screen 0 1366x768x16 &" >> /usr/src/app/Xvfb.start
RUN echo "export DISPLAY=99.0" >> /usr/src/app/Xvfb.start
RUN chmod +x /usr/src/app/Xvfb.start

# Fetch geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && tar -xvzf geckodriver-v0.26.0-linux64.tar.gz && mv geckodriver /usr/local/bin/geckodriver


COPY . .
CMD ["./app.sh"]

