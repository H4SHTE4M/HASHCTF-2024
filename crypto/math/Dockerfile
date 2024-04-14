FROM python:3
LABEL Description="Game" VERSION='1.0'

WORKDIR /opt/game
RUN mkdir -p /opt/game

COPY task.py .
COPY secret.py .

#RUN pip install pycryptodome

EXPOSE 10000
CMD ["python", "-u", "task.py"]

