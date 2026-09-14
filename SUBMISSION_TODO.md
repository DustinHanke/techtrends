# Submission TODO

The code/configuration portion of the project is prepared. The following items require your own external accounts or local Kubernetes environment and therefore must be completed before submission:

1. Create GitHub repository secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.
2. Push the project to GitHub on the `main` branch and verify the `TechTrends - Package with Docker` workflow succeeds.
3. Replace `YOUR_GITHUB_USERNAME/YOUR_REPOSITORY` in both `argocd/*.yaml` files with the repository that contains this Helm chart.
4. Make sure the Kubernetes/Helm image repository points to the image your cluster can actually pull. The rubric defaults use `techtrends:latest`; when pulling from DockerHub this will normally be `<dockerhub-user>/techtrends:latest`.
5. Run the Docker container, exercise the site, and paste the real output of `docker logs techtrends` into `docker_commands`.
6. Add the required screenshots to `screenshots/`:
   - `docker-run-local`
   - `ci-github-actions`
   - `ci-dockerhub`
   - `k8s-nodes`
   - `kubernetes-declarative-manifests`
   - `argocd-ui`
   - `argocd-techtrends-staging`
   - `argocd-techtrends-prod`
7. Verify staging has 3 replicas and production has 5 replicas after ArgoCD synchronization.

Do not replace the screenshot/log placeholders with fabricated evidence; they should come from your own successful runs.
