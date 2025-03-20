FROM ubuntu:20.04

RUN apt update
RUN apt install -y xinetd
RUN apt install -y qemu-user-static

COPY --chmod=755 iot-shell /iot-shell
COPY --chmod=755 iotup.sh /iotup.sh
COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=755 service.sh /service.sh
COPY --chmod=755 sysroot /sysroot

