# Getting Started

## 1. Clone the repository
```bash
git clone https://github.com/adrianwalker/pact-hackday.git
```

## 2. Change directory to the project root
```bash
cd pact-hackday
```

## 3. Install dependencies with poetry
```bash
poetry install
```

## 4. Start a PACT broker with docker
```bash
docker compose up -d pact-broker
```
## 5. Run tests with pytest
```bash
poetry run pytest
```

## 6. View PACTs in the PACT broker

http://localhost:9292/

