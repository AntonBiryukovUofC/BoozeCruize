FROM python:3

WORKDIR /usr/src/app
CMD mkdir panel_app
WORKDIR /usr/src/app/panel_app

copy requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["./app.sh"]

