# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application, which consists of a frontend and backend service.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- The Docker images `todo-frontend:latest` and `todo-backend:latest` must be available in your cluster

## Configuration

The following table lists the configurable parameters of the todo-chatbot chart and their default values.

### Backend Parameters

| Parameter                    | Description                                      | Default                             |
| ---------------------------- | ------------------------------------------------ | ----------------------------------- |
| `backend.replicaCount`       | Number of backend replicas                       | `1`                                 |
| `backend.image.repository`   | Backend image repository                         | `todo-backend`                      |
| `backend.image.pullPolicy`   | Backend image pull policy                        | `IfNotPresent`                      |
| `backend.image.tag`          | Backend image tag                                | `latest`                            |
| `backend.service.type`       | Backend service type                             | `ClusterIP`                         |
| `backend.service.port`       | Backend service port                             | `8000`                              |
| `backend.service.targetPort` | Backend target port                              | `8000`                              |
| `backend.env.DATABASE_URL`   | Database URL for the backend                     | `sqlite:///./todo.db`               |
| `backend.env.BETTER_AUTH_SECRET` | Authentication secret for the backend        | `supersecretkeyforauthentication`   |
| `backend.env.PORT`           | Port for the backend to listen on                | `8000`                              |

### Frontend Parameters

| Parameter                    | Description                                      | Default                             |
| ---------------------------- | ------------------------------------------------ | ----------------------------------- |
| `frontend.replicaCount`      | Number of frontend replicas                      | `1`                                 |
| `frontend.image.repository`  | Frontend image repository                        | `todo-frontend`                     |
| `frontend.image.pullPolicy`  | Frontend image pull policy                       | `IfNotPresent`                      |
| `frontend.image.tag`         | Frontend image tag                               | `latest`                            |
| `frontend.service.type`      | Frontend service type                            | `LoadBalancer`                      |
| `frontend.service.port`      | Frontend service port                            | `3000`                              |
| `frontend.service.targetPort`| Frontend target port                             | `3000`                              |
| `frontend.env.NEXT_PUBLIC_API_URL` | API URL for the frontend to connect to backend | `http://backend-service:8000`     |
| `frontend.env.PORT`          | Port for the frontend to listen on               | `3000`                              |

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
# From the todo-app directory
helm install my-release ./todo-bot
```

The command deploys the todo-chatbot application on the Kubernetes cluster with the default configuration. The [Parameters](#parameters) section lists the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Customizing the Chart

You can override the default values by creating a custom `values.yaml` file and passing it during installation:

```bash
helm install my-release ./todo-bot -f my-values.yaml
```

Or by specifying individual parameters:

```bash
helm install my-release ./todo-bot --set backend.replicaCount=2 --set frontend.service.type=NodePort
```