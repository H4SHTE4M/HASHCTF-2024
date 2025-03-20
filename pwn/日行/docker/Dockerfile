FROM ubuntu:20.04

RUN apt update
RUN apt install -y xinetd

COPY --chmod=755 iot-shell /iot-shell
COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=755 service.sh /service.sh

CMD ["/service.sh"]
