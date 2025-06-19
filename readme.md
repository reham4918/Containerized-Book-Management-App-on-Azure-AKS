# 📚 Containerized Book Management App on Azure AKS

A modern book management system deployed on Azure Kubernetes Service (AKS) with MongoDB backend. This application allows you to manage your book inventory with features like adding, updating, searching, and soft/permanent deletion of books.

## 🌟 Features

- 📖 Full CRUD operations for book management
- 🔍 Search functionality by ISBN, title, or author
- 🗑️ Soft delete with restore capability
- 🎨 Modern and responsive UI
- 🔐 MongoDB integration with Azure Cosmos DB
- 🚀 Containerized deployment on Azure AKS
- ⚖️ Load balanced service
- 🔄 Multiple replicas for high availability

## 🛠️ Tech Stack

- **Frontend**: HTML, Bootstrap 5, JavaScript
- **Backend**: Python Flask
- **Database**: MongoDB (Azure Cosmos DB)
- **Container**: Docker
- **Orchestration**: Kubernetes (AKS)
- **Registry**: Azure Container Registry

## 🚀 Local Development

### Prerequisites

- Docker
- Python 3.x
- MongoDB
- Azure CLI (for deployment)

### Running Locally with Docker

1. Build the Docker image:
```bash
docker build -t bookstore-project .
```

2. Run the container:
```bash
docker run --detach --publish 5000:5000 --name bookstore-project bookstore-project
```

The application will be available at `http://localhost:5000`

## 📦 Azure Container Registry (ACR) Setup

1. Tag the image for ACR:
```bash
docker tag bookstore-project:latest <your-acr>.azurecr.io/bookstore-project:latest
```

2. Push to ACR:
```bash
docker push <your-acr>.azurecr.io/bookstore-project:latest
```

3. Verify the image in registry:
```bash
az login
az acr repository list --name <your-acr> --output table
```

4. Enable anonymous pull (if needed):
```bash
az acr update -n <your-acr> --anonymous-pull-enabled true
```

## 🌐 AKS Deployment

1. Get AKS credentials:
```bash
az aks get-credentials --resource-group <your-resource-group> --name <your-aks-cluster>
```

2. Apply Kubernetes configurations:
```bash
kubectl apply -f aks_deployment/secret.yaml
kubectl apply -f aks_deployment/deployment.yaml
kubectl apply -f aks_deployment/service.yaml
```

### 🔍 Troubleshooting

If you encounter `ImagePullBackOff` error on ARM-based machines:
```bash
docker buildx build --platform linux/amd64 -t <your-acr>.azurecr.io/bookstore-project:latest .
docker push <your-acr>.azurecr.io/bookstore-project:latest
```

## 📋 Application Structure

```
.
├── app.py                  # Main Flask application
├── templates/             # HTML templates
│   ├── book_details.html  # Book details view
│   ├── form.html         # Add book form
│   ├── index.html        # Main page
│   ├── search_results.html # Search results
│   └── update_book.html  # Update book form
├── aks_deployment/       # Kubernetes configurations
│   ├── deployment.yaml   # Deployment configuration
│   ├── secret.yaml      # MongoDB connection secret
│   └── service.yaml     # Service configuration
└── Dockerfile           # Docker configuration
```

## 🔐 Environment Variables

- `MONGO_URI`: MongoDB connection string (stored in Kubernetes secret)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
