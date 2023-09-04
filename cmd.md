Build Docker :
```bash
docker build -t crous-api .
```

Run Docker :
```bash
docker run -p 80:8080 --env-file .env -d crous-api
```