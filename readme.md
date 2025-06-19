# docker test app locally

```
docker build -t bookstore-project .
docker run --detach --publish 5000:5000 --name bookstore-project bookstore-project
```

# upload to azure container registry

```
docker tag bookstore-project:latest bookstore-project.azurecr.io/bookstore-project:latest
docker push bookstore-project.azurecr.io/bookstore-project:latest
```

```
docker login rhmprojectcr.azurecr.io -u rhmprojectcr -p L8m/pexTklqugQDCopfSbkt3g0DWI4Zn7PTE4/kQ+N+ACRAwzYrX
docker tag bookstore-project rhmprojectcr.azurecr.io/bookstore-project:latest
docker image push rhmprojectcr.azurecr.io/bookstore-project:latest
```

Verify the image is in the registry


```
az login
az acr repository list --name rhmprojectcr --output table
```


enable annonymous pull
```
az acr update -n rhmprojectcr --anonymous-pull-enabled true
```

check if it is enabled
```
az acr show -n rhmprojectcr --query "anonymousPullEnabled" -o tsv
```


# deploy to aks

```
az aks get-credentials --resource-group project_rg --name rhmprojectaks
kubectl apply -f aks_deployment/secret.yaml
kubectl apply -f aks_deployment/deployment.yaml
kubectl apply -f aks_deployment/service.yaml
```

# debug error ImagePullBackOff

```
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

error: 
```
Failed to pull image "rhmprojectcr.azurecr.io/bookstore-project:latest": rpc error: code = NotFound desc = failed to pull and unpack image "rhmprojectcr.azurecr.io/bookstore-project:latest": no match for platform in manifest: not found
```

need to build the image with the correct platform

```
docker buildx build --platform linux/amd64 -t rhmprojectcr.azurecr.io/bookstore-project:latest .
docker push rhmprojectcr.azurecr.io/bookstore-project:latest
```

# deploy to aks again

```
az aks get-credentials --resource-group project_rg --name rhmprojectaks
kubectl apply -f aks_deployment/secret.yaml
kubectl apply -f aks_deployment/deployment.yaml
kubectl apply -f aks_deployment/service.yaml
```





