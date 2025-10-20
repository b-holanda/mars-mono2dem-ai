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
sudo apt install -y gdal-bin libgdal-dev python3-gdal zip unzip
```

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

