# shop-api: a small DevOps learning project

A small Flask API packaged with Docker, tested with pytest, scanned in GitHub Actions, and accompanied by Kubernetes manifests and an nginx 5xx log-analysis script.

## What it demonstrates

- Flask API with `/`, `/health`, and `/products` endpoints
- Pinned Python base image and pinned Python dependencies
- Docker image runs as a non-root user
- Docker Compose for local container execution
- GitHub Actions: tests → Docker build → Trivy vulnerability scan
- On pushes to `main`, publishes a commit-SHA-tagged image to GHCR
- Kubernetes Deployment (3 replicas, rolling update, probes, resource requests/limits) and internal ClusterIP Service
- Python script to report the top five client IPs with HTTP 5xx responses

> The workflow publishes an image to GHCR on `main`. The final deployment step is intentionally a placeholder: no Kubernetes cluster or production credentials are assumed.

## Run locally

Requires Python 3.12+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
pip install pytest
pytest -q
python -m gunicorn --bind 0.0.0.0:5000 app:app
```

Open `http://127.0.0.1:5000/health`.

## Run with Docker

```bash
docker build -t shop-api:local .
docker run --rm -p 5000:5000 shop-api:local
```

Or use Docker Compose:

```bash
docker compose up --build
```

Then check `http://localhost:5000/health`. Stop Compose with `Ctrl+C`, then `docker compose down`.

## Log analysis

```bash
python scripts/analyze_logs.py sample-access.log
```

The script reads the client IP from field 1 and HTTP status from field 9, counts only 500–599 responses, and prints the five highest counts.

## Kubernetes

Update the image in `k8s/shop-api.yaml` to the image published in your GHCR package, then run:

```bash
kubectl apply -f k8s/shop-api.yaml
kubectl rollout status deployment/shop-api
kubectl get pods -l app=shop-api
kubectl get service shop-api
```

The Service is internal to the cluster (`ClusterIP`) on port 80 and forwards to container port 5000. To test locally:

```bash
kubectl port-forward service/shop-api 8080:80
```

Then open `http://127.0.0.1:8080/health`.

## GitHub Actions and GHCR

1. Create a public GitHub repository named `shop-api-devops`.
2. Push this project to the `main` branch.
3. Open the **Actions** tab and inspect the workflow run.
4. The workflow runs tests, builds the image using the commit SHA, and scans it with Trivy.
5. On a push to `main`, it also publishes `ghcr.io/<owner>/shop-api:<commit-sha>` using the built-in `GITHUB_TOKEN`.

The workflow needs the repository's Actions permission to read and write packages. If GHCR publication is denied, check **Settings → Actions → General → Workflow permissions** and allow read and write permissions.

## Troubleshooting notes

- **Container exits:** inspect `docker logs <container>` and confirm Gunicorn can import `app:app`.
- **Port unavailable:** check whether another process is already using host port 5000.
- **Kubernetes pod not ready:** run `kubectl describe pod <pod>` and `kubectl logs <pod> --previous`; verify `/health` responds on port 5000.
- **Trivy fails:** review the reported CVEs and update the affected base image or dependency deliberately; do not disable the scan just to get a green run.

## Scope and limitations

This is a learning/demo service, not a production commerce backend. It has no database, authentication, secrets, ingress, TLS, autoscaling, or real cluster deployment. The Kubernetes image placeholder must be replaced with your own published image before applying the manifest.
