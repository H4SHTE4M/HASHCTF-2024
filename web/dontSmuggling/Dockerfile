FROM mitmproxy/mitmproxy:6.0.2
WORKDIR /app
RUN pip3 install -v gunicorn==20.0.4
RUN pip3 install -v mitmproxy==6.0.2
RUN pip3 install Flask-AutoIndex
COPY ./src .
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT [ "/docker-entrypoint.sh" ]
