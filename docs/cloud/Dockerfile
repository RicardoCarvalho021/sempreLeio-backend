FROM python:3
RUN apt-get update
RUN python -m pip install --upgrade pip
WORKDIR /srv/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x run.sh
EXPOSE 8000