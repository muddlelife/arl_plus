# syntax=docker/dockerfile:1
# ARL unified Dockerfile — works for both amd64 and arm64.
# Build:  docker build -t arl:local .
# Or:     docker compose up -d --build

# -------------------------------------------------------------------
# Stage 1: compile massdns for the target architecture
# -------------------------------------------------------------------
FROM debian:12 AS massdns-builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      g++ make git ca-certificates libssl-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/blechschmidt/massdns.git /opt/massdns \
    && cd /opt/massdns && make

# -------------------------------------------------------------------
# Stage 2: main runtime
# -------------------------------------------------------------------
FROM python:3.11-slim-bookworm

ARG TARGETARCH=amd64
WORKDIR /code

# ---- system packages ------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      nginx \
      nmap \
      ncrack \
      curl \
      wget \
      unzip \
      openssl \
      bash \
      netcat-openbsd \
      ca-certificates \
      git \
      fontconfig \
      fonts-wqy-microhei \
      build-essential \
      python3-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- app code -------------------------------------------------------
COPY app/ app/
COPY test/ test/

# massdns binary (cross-compiled in stage 1 for any arch)
COPY --from=massdns-builder /opt/massdns/bin/massdns app/tools/massdns

COPY docker/frontend/ frontend/
COPY docker/nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /code/app/tools/* || true

# ---- helpers --------------------------------------------------------
COPY docker/worker/gen_crt.sh /usr/bin/gen_crt.sh
COPY docker/worker/wait-for-it.sh /usr/bin/wait-for-it.sh
RUN chmod +x /usr/bin/gen_crt.sh /usr/bin/wait-for-it.sh

# ---- ARL-NPoC -------------------------------------------------------
ARG ARL_NPOC_REPO=https://github.com/Aabyss-Team/ARL-NPoC
ARG ARL_NPOC_REF=master
RUN git clone --depth 1 --branch ${ARL_NPOC_REF} ${ARL_NPOC_REPO} /opt/ARL-NPoC

WORKDIR /opt/ARL-NPoC/
RUN python -m pip install --no-cache-dir -e .

WORKDIR /code

# ---- SSL dhparam ----------------------------------------------------
RUN curl -fsSL https://ssl-config.mozilla.org/ffdhe2048.txt -o /etc/ssl/certs/dhparam.pem

# ---- GeoLite2 -------------------------------------------------------
COPY requirements.txt requirements.txt
RUN mkdir -p /data/GeoLite2
ARG GEOLITE2_ASN_URL=https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb
ARG GEOLITE2_CITY_URL=https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb
RUN wget -q -O /data/GeoLite2/GeoLite2-ASN.mmdb  ${GEOLITE2_ASN_URL} \
    && wget -q -O /data/GeoLite2/GeoLite2-City.mmdb ${GEOLITE2_CITY_URL}

# ---- Python dependencies --------------------------------------------
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /opt/ARL-NPoC/
RUN sed -i 's/^PyYAML==5\.4\.1$/PyYAML==6.0.2/' requirements.txt \
    && python -m pip install --no-cache-dir -r requirements.txt

# ---- nuclei (arch-aware) --------------------------------------------
ARG NUCLEI_VERSION=3.2.4
RUN NUCLEI_ARCH="${TARGETARCH}" \
    && echo "Installing nuclei v${NUCLEI_VERSION} for ${NUCLEI_ARCH}" \
    && wget -q "https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_${NUCLEI_ARCH}.zip" \
    && unzip -q "nuclei_${NUCLEI_VERSION}_linux_${NUCLEI_ARCH}.zip" nuclei \
    && mv nuclei /usr/bin/ \
    && rm -f "nuclei_${NUCLEI_VERSION}_linux_${NUCLEI_ARCH}.zip" \
    && nuclei -ut

# ---- wih (arch-aware) -----------------------------------------------
RUN WIH_ARCH="${TARGETARCH}" \
    && echo "Installing wih for ${WIH_ARCH}" \
    && wget -q "https://github.com/Aabyss-Team/arl_files/raw/master/wih/wih_linux_${WIH_ARCH}" -O /usr/bin/wih \
    && chmod +x /usr/bin/wih \
    && wih --version

# ---- admin init helper -----------------------------------------------
COPY docker/worker/init_admin.py /usr/bin/init_admin.py
RUN chmod +x /usr/bin/init_admin.py

# ---- smoke check ----------------------------------------------------
WORKDIR /code
RUN cp app/config.yaml.example app/config.yaml \
    && env FLASK_APP=app.main:arl_app python -m flask routes
