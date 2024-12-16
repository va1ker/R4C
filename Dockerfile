FROM python:3.12
RUN apt update \ 
    && apt install -y 
WORKDIR /app
COPY requirements.txt requirements-dev.txt /app/
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8000