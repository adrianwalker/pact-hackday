Getting started

1) Clone the repo:

git clone https://github.com/adrianwalker/pact-hackday.git

2) Change directory to the project root:

cd pact-hackday

3) Install dependencies with poetry:

poetry install

4) Start a PACT broker with docker:

docker compose up -d pact-broker

5) Run tests with pytest:

pytest

6) View PACTs in the PACT broker:

http://localhost:9292/

