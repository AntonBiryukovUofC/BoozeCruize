FROM python:3

WORKDIR /usr/src/app
CMD mkdir panel_app
WORKDIR /usr/src/app/panel_app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && tar -xvzf geckodriver-v0.26.0-linux64.tar.gz

COPY . .
CMD ["./app.sh"]

