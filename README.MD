
# About

This is the support project for managing interactions between junior and senior specialists, where Juniors can ask questions and Seniors provide answers in a controlled workflow with predefined statuses.

## Pipenv Usage

The project uses `pipenv` as the main package manager. For more detailed instructions, please refer to the 🔗 [Pipenv documentation](https://pipenv.pypa.io/en/latest/).

### Creating a new virtual environment

pipenv shell


### Creating a `.lock` file from `Pipenv` file
pipenv lock


### Installing dependencies from the `.lock` file

pipenv sync

## 🐳 Deploy with Docker Compose

1. Copy the default environment file:

cp .env.default .env

2. Build and start the containers:

docker compose build && docker compose up -d


## Some Useful Commands

### View the last 20 lines of logs and follow the output

docker compose logs --tail 20 -f api


### Execute a command inside the container

docker compose exec api <command>

