# Image Transfer

This is a lightweight CLI tool to automate container image transfers between registries using `docker` or `podman`

## Features

- Pull, tag, and push container images between registries
- Configurable via a simple `config.yaml` file
- Uses `uv` for fast dependency management and clean Python environments

## About files within the directory

transfer-images/ 
│
├── transferimages.py -> Main script to handle image transfer 
├── config.yaml  -> YAML file defining source and destination image pairs 
├── pyproject.toml  -> Project metadata and dependencies (uv-compatible) 
├── uv.lock -> Locked dependencies 
└── README.md  -> Documentation

## Prerequisites

- Python 3.13+
-  Install [`uv`](https://github.com/astral-sh/uv)  
	macOs or Linux :

```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
```
    Windows :
		
```powershell

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- Install Docker or Podman and ensure that it is accesible via CLI.

## Getting Started :

### 1. Clone the Repository

```bash
git clone git@github.com:Roshani-Udupa/transfer-images.git
cd transfer-images
```

### 2. Set Up the Virtual Environment

```bash
uv venv
```
Activate the virtual environment:
```bash
source .venv/Scripts/activate
```
Install the dependencies:
```bash
uv pip install .
```
 
### 3. Configure Image Transfers

Edit the `config.yaml` to specify which images to transfer:

```yaml
transfers:
  - source: docker.io/library/ubuntu:latest
    destination: quay.io/yourorg/ubuntu:latest
  - source: docker.io/library/nginx:latest
    destination: my-registry.io/library/nginx:latest
```

### 4. Run the Script

```bash
python transferimages.py
```
 Or
 ```bash
 uv run transferimages.py
```

You'll be prompted to choose between `docker` or `podman`.
Example:

```bash
Enter the Command Line Tool you want to use to transfer images (docker/podman): podman
```