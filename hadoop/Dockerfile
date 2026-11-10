
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java, Python, SSH y herramientas
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    openssh-server \
    curl \
    ca-certificates \
    procps \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Configurar Java y Hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_VERSION=3.4.1
ENV HADOOP_HOME=/opt/hadoop
ENV PATH="${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin"

# Descargar e instalar Hadoop
RUN mkdir -p ${HADOOP_HOME} /run/sshd && \
    curl -fsSL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    -o /tmp/hadoop.tar.gz && \
    tar -xzf /tmp/hadoop.tar.gz -C ${HADOOP_HOME} --strip-components=1 && \
    rm /tmp/hadoop.tar.gz

# Crear usuario para Hadoop
RUN useradd -m -s /bin/bash hadoop && \
    mkdir -p /home/hadoop/.ssh && \
    chmod 700 /home/hadoop/.ssh && \
    chown -R hadoop:hadoop /home/hadoop

# Configurar SSH
RUN ssh-keygen -A && \
    echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config

# Configurar Java para Hadoop
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

WORKDIR /workspace

EXPOSE 22

CMD ["bash", "-c", "service ssh start && tail -f /dev/null"]
