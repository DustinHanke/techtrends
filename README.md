# TechTrends Web Application

TechTrends is a Flask news-sharing application packaged and deployed using Docker, Kubernetes, Helm, GitHub Actions, and ArgoCD.

## Run locally with Python

```bash
python init_db.py
python app.py
```

The application listens on `http://127.0.0.1:3111`.

Health and metrics endpoints:

```bash
curl http://127.0.0.1:3111/healthz
curl http://127.0.0.1:3111/metrics
```

## Docker

Commands required by the project are recorded in `docker_commands`.

```bash
docker build -t techtrends -f Dockerfile .
docker run -d --name techtrends -p 7111:3111 techtrends
```

Then open `http://127.0.0.1:7111`.

## GitHub Actions / DockerHub

The workflow `.github/workflows/techtrends-dockerhub.yml` expects these repository secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Every push to `main` builds and pushes both `latest` and a commit-SHA image tag.

## Kubernetes

Declarative manifests are in `kubernetes/`.

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deploy.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get all -n sandbox
```

## Helm

The Helm chart is stored in `helm/`.

```bash
helm template techtrends ./helm
helm template techtrends-staging ./helm -f helm/values-staging.yaml
helm template techtrends-prod ./helm -f helm/values-prod.yaml
```

## ArgoCD

Before applying the ArgoCD Application manifests, replace `YOUR_GITHUB_USERNAME/YOUR_REPOSITORY` in both files under `argocd/` with the public GitHub repository containing this project.

```bash
kubectl apply -f argocd/helm-techtrends-staging.yaml
kubectl apply -f argocd/helm-techtrends-prod.yaml
```

## Required screenshots

Add the following screenshots to `screenshots/` before submission:

- `docker-run-local`
- `ci-github-actions`
- `ci-dockerhub`
- `k8s-nodes`
- `kubernetes-declarative-manifests`
- `argocd-ui`
- `argocd-techtrends-staging`
- `argocd-techtrends-prod`

## Standout functionality implemented

- Dynamic `/healthz`: returns HTTP 500 with `ERROR - unhealthy` when the database/posts table cannot be queried.
- Custom Docker tags: the GitHub Actions workflow pushes `latest` plus a SHA-derived tag.
- Helm service fallback: `targetPort` defaults to the configured service `port` when no explicit target port is supplied.
