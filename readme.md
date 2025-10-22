# mars-mono2dem-ai

Pipeline experimental para ingestão, análise e padronização de pares HiRISE (ORI/DTM) inteiramente em disco local.

## Requisitos

- Linux (testado em Ubuntu 22.04)
- Python 3.12
- [GDAL](https://gdal.org/) com drivers JP2/GeoTIFF ativos
- Chromium (utilizado pelos componentes de automação)
- VS Code (opcional, mas recomendado)

## Setup

### Gdal

```bash
sudo apt update
```

```bash
sudo apt install -y gdal-bin \
  libgdal-dev \
  python3-gdal \
  zip \
  unzip \
  python3.12-venv \
  python-is-python3 \
  python3-dev \
  build-essential \
  g++ \
  libproj-dev \
  proj-bin \
  libgeos-dev \
  libtiff-dev \
  libopenjp2-7 \
  libopenjp2-7-dev \
  libjpeg-dev \
  libzstd-dev \
  libdeflate-dev
```
```bash
export GDAL_CONFIG=/usr/bin/gdal-config
````
### Python env

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

### Install packages

```bash
pip install -r requirements.txt
```

### Run CLI

```bash
 python -m cli help
```

### Run CLI interactive mode
```bash
 python -m cli
```

