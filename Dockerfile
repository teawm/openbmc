FROM ubuntu:22.04

# Убираем интерактивные запросы при установке пакетов
ENV DEBIAN_FRONTEND=noninteractive

# Установка QEMU и базовых утилит
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    qemu-system-arm \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Открываем порты
EXPOSE 22 443 623

# Запускаем QEMU
CMD ["qemu-system-arm", \
    "-m", "256", \
    "-M", "romulus-bmc", \
    "-nographic", \
    "-drive", "file=romulus/obmc-phosphor-image-romulus-20251118122033.static.mtd,format=raw,if=mtd", \
    "-net", "nic", \
    "-net", "user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu"]