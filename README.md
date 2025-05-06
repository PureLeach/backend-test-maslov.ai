# 📚 GraphQL Books API

A simple application on FastAPI + Strawberry GraphQL to retrieve a list of books and authors from PostgreSQL.

## 🚀 Technologies used

- Python 3.12+
- FastAPI
- Strawberry (GraphQL)
- PostgreSQL
- Databases
- asyncpg
- yoyo (migrations)
- ruff
- mypy
- docker-compose


## 📦 Installation and startup

1. **Clone the repository:**

```bash
git clone https://github.com/PureLeach/backend-test-maslov.ai.git
cd backend-test-maslov.ai
````

2. **Create and activate a virtual environment:**

```bash
poetry shell
```

3. **Install dependencies:**

```bash
poetry install
```

4. **Create'.env` or specify the environment variables:**


```bash
cp .env.example .env
```

5. **Run PostgreSQL and apply migrations**

```bash
docker-compose up -d
make migrate
```

6. **Start the app:**

```bash
make run
```

7. **Open GraphQL Playground:**

Go to the browser: [http://localhost:8000/graphql](http://localhost:8000/graphql)

---

## 🔍 Examples of requests

### 1. Get all the books
```graphql
query {
  books {
    title
    author {
      name
    }
  }
}
```

### 2. Get books by author (e.g., Oscar Wilde - ID = 1)
```graphql
query {
  books(authorIds: [1]) {
    title
    author {
      name
    }
  }
}
```

### 3. Search for books by part of title (case is not important)
```graphql
query {
  books(search: "adventures") {
    title
    author {
      name
    }
  }
}
```

### 4. Get no more than 2 books
```graphql
query {
  books(limit: 2) {
    title
    author {
      name
    }
  }
}
```

### 5. Combination of all filters
```graphql
query {
  books(authorIds: [3], search: "Adventures", limit: 1) {
    title
    author {
      name
    }
  }
}
```

### 6. No match (empty result)
```graphql
query {
  books(search: "Nonexistent") {
    title
    author {
      name
    }
  }
}
```
