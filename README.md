# `dbt-core` Airflow Tutorial

dbt-core Airflow template in PostgreSQL and podman

[![Generic badge](https://img.shields.io/badge/dbt-1.8.8-blue.svg)](https://docs.getdbt.com/dbt-cli/cli-overview)
[![Generic badge](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Generic badge](https://img.shields.io/badge/Python-3.11.10-blue.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/Podman-5.0.2-blue.svg)](https://www.docker.com/)

In this tutorial, for the purpose of `dbt-core` exercises, I made some modifications to the `profiles.yml` file to use the local `PostgreSQL` repository.

- [`dbt-core` Airflow Tutorial](#dbt-core-airflow-tutorial)
  - [Preparation](#preparation)
    - [Prerequisites](#prerequisites)
    - [Install podman in WSL2 Ubuntu 20.04](#install-podman-in-wsl2-ubuntu-2004)
    - [Set Podman’s Docker-Compatible API Service in WSL Ubuntu](#set-podmans-docker-compatible-api-service-in-wsl-ubuntu)
    - [Install Astro CLI](#install-astro-cli)
    - [Create repository](#create-repository)
    - [Create venv with dbt](#create-venv-with-dbt)
    - [Start database](#start-database)
    - [Project Set Up](#project-set-up)
  - [Deployment](#deployment)
    - [Overview](#overview)
    - [dbt-core](#dbt-core)

## Preparation

### Prerequisites

Astro CLI

- install on WSL2 linux

dbt tutorial

- Python/conda
- Podman desktop
- DBeaver
- git client
- Visual Code

### Install podman in WSL2 Ubuntu 20.04
  
- Ref to [Podman Installation on Ubuntu](https://gist.github.com/nikAizuddin/1c1822bd32b3c449433d0f81f796b71d)
- install Podman:

  ```bash
  sudo apt update
  sudo apt install ca-certificates
  . /etc/os-release
  echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
  curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key | sudo apt-key add -
  sudo apt update
  sudo apt -y upgrade
  sudo apt -y install podman
  ```

- initialize rootless Podman:

```bash
podman info
```

- create config

```bash
sudo cp -v /usr/share/containers/containers.conf /etc/containers/

```

- update /etc/containers/containers.conf

  - Change cgroup_manager = "systemd" to cgroup_manager = "cgroupfs"
  - Change events_logger = "journald" to events_logger = "file"
  - Increase ulimits to 65535 and make memlock unlimited:

  ```
  [containers]
  default_ulimits = [ 
    "nofile=65535:65535",
    "memlock=-1:-1"
  ]

  ```

- update ~/.config/containers/containers.conf

```
[containers]
default_ulimits = []

```

- IPv4 forwarding
  - create ~/.config/containers

  ```bash
  mkdir ~/.config/containers

  ```
  
  - update ***/etc/containers/containers.conf***

  ```
  [containers]
  default_sysctls = [
  "net.ipv4.ping_group_range=0 0",
  "net.ipv4.ip_forward=1"
  ]  

  ```

- set max virtual memory regions that single process can use
  - max_map_count, at least 262144
  - update /etc/sysctl.conf

  ```
  vm.max_map_count=300000

  ```

  - To apply vm.max_map_count
  ```bash
  sudo sysctl -w vm.max_map_count=300000

  ```

### Set Podman’s Docker-Compatible API Service in WSL Ubuntu

Default podman remote connect is ssh, but Astro required unix.

- Start Podman’s Docker-Compatible API Service Manually

```command
podman system service --time=0 tcp:0.0.0.0:12345
```

- Set the DOCKER_HOST Environment Variable in WSL

```command
export DOCKER_HOST=tcp://localhost:12345
```

- To make this change persistent

```command
echo 'export DOCKER_HOST=tcp://localhost:12345' >> ~/.bashrc
source ~/.bashrc
```

- Start podman service

```command
podman system service --time=0 tcp:0.0.0:12345 &

```


### Install Astro CLI

- Install Astro CLI on linux

```bash
curl -sSL install.astronomer.io | sudo bash -s
```

- [Run the Astro CLI using Podman](https://www.astronomer.io/docs/astro/cli/use-podman?tab=windows#configure-the-astro-cli-to-use-podman)
  -  confirm that Podman has access images  


  ```bash
  podman run --rm -it postgres:12.6 whoami
  ```

  - set Podman as your container management engine

  ```bash
  astro config set -g container.binary podman
  astro config set -g duplicate_volumes false
  ```


- Optional, Install Astro CLI on Windows

  - Open Windows PowerShell as an administrator and then run the following command:

  ```command
  winget install -e --id Astronomer.Astro
  ```

  - Restart Shell and run ```astro version``` to confirm the Astro CLI is installed properly.



### Create repository

1. Create a new GitHub repository

- Find our Github template repository [dbt-fundamental-template](https://github.com/saastoolset/dbt-fundamental-template)
- Click the big green 'Use this template' button and 'Create a new repository'.
- Create a new GitHub repository named **dbt-fund-ex1**.

![Click use template](.github/static/use-template.gif)

1. Select Public so the repository can be shared with others. You can always make it private later.
2. Leave the default values for all other settings.
3. Click Create repository.
4. Save the commands from "…or create a new repository on the command line" to use later in Commit your changes.
5. Install and setup envrionment

### Create venv with dbt

Skip this step if already create dbt venv

- Create python virtual env for dbt
  - For venv and and docker, using the [installation instructions](https://docs.getdbt.com/docs/core/installation-overview) for your operating system.
  - For conda in Windows, open conda prompt terminal in ***system administrador priviledge***

  ```command
  conda create -n dbt dbt-core dbt-postgres
  conda activate dbt
  ```

### Start database

- Start up db and pgadmin
  . use admin/Passw0rd as connection

  ```command
  cd C:\Proj\myProj\50-GIT\dbt-fund-ex1
  bin\db-start-pg.bat
  ```

### Project Set Up

- Init project in repository home directory
  Initiate the jaffle_shop project using the init command:

```command
dbt init jaffle_shop
```

- Connect to PostgreSQL

  - Update `profiles.yml`
  Now we should create the `profiles.yml` file on the `C:\Users\YourID\.dbt` directory. The file should look like this:

```YAML
config:
    use_colors: True 
jaffle_shop:
  outputs:
    dev:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: "admin"
      pass: "Passw0rd"
      dbname: raw
      schema: jaffle_shop
    prod:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: "admin"
      pass: "Passw0rd"
      dbname: raw
      schema: analytics
  target: dev
```

- Test connection config

```
cd jaffle_shop
dbt debug
```


## Deployment

### Overview

  Development in dbt is the process of building, refactoring, and organizing different files in your dbt project. 

- This is done in a development environment using a development schema (dbt_jsmith) and typically on a non-default branch (i.e. feature/customers-model, fix/date-spine-issue). After making the appropriate changes, the development branch is merged to main/master so that those changes can be used in deployment.
- Deployment in dbt (or running dbt in production) is the process of running dbt on a schedule in a deployment environment. The deployment environment will typically run from the default branch 

### dbt-core

- Scheduling of future jobs can run by Airflow or other scheduler

  - run airflow

  ```command
  astro dev start
  ```


  - stop airflow

  ```command
  astro dev stop
  ```
