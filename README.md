# VISA Kubernetes Cloud Provider — PoC

This repository contains a Proof of Concept (PoC) for a Kubernetes cloud provider for VISA. It enables orchestration of
instances on the [VISA platform](https://visa.readthedocs.io/en/latest/index.html) through a Kubernetes-based backend.

The solution implements a REST API middleware between a Kubernetes cluster and VISA, allowing Kubernetes to manage VISA
resources as if they were native cloud infrastructure.

Integration with VISA is achieved via the **[Alternative Cloud Provider interface](https://visa.readthedocs.io/en/latest/development/development-cloud-provider.html)**.

---

## TL;DR

This is a **Proof of Concept** and not yet a final fully-production-grade solution.

While it can be deployed in production environments, the current approach is intended for experimentation and
validation. A more robust implementation based on Kubernetes Operators and Custom Resource Definitions (CRDs) is
currently under development and is expected to eventually replace this project.

For more information about ongoing developments, please contact the **MIS section at ALBA Synchrotron**.

## Building container images for VISA

Under the `visa_container_images` directory, you can find the Dockerfile for building a container image for using is
VISA. It can be used as a base image and extend from it to install scientific software on top of it.

The image installs and configures the additional VISA extension for authentication and
printing, [VISA PAM](https://github.com/ILLGrenoble/visa-pam)
and [VISA CUPS](https://github.com/ALBA-Synchrotron/visa-cups), respectively.

The VISA CUPS module has been forked and slightly modified to work with this implementation.

In order for the VISA PAM module to correctly work, in the namespace the pods are going to be deployed, there must exist
a config map containing the public key for validating the authentication tokens. The name of the config map changes
depending on the environment (see `VISA_PUBLIC_KEY_NAME` on `settings_test.py` and `settings_prod.py`).

```yaml
apiVersion: v1
data:
  public.key: |
    -----BEGIN PUBLIC KEY-----
    AAAAddddAAA...
    -----END PUBLIC KEY-----
kind: ConfigMap
metadata:
  name: test-pam-key
  namespace: visa-pods-test
```

This modified VISA PAM module is configured to find the public key in the path the cloud provider mounts it in the
provisioned instances.

## Implementation

The backend is built in Python, using Django and Django's REST framework and a MariaDB database.

On the [2025 PaN Facilities VISA Meeting](https://indico.cells.es/event/1639/overview) a presentation was given about
this implementation. The
presentation [slides](https://indico.cells.es/event/1639/contributions/2992/attachments/1881/4154/VISA_k8s_cloud_provider_ALBA.pdf)
contain additional details on the implementation and operation of this backend.

## Configuration

### Database

Configuration of the MariaDB database is done through `/django/config/database/my.cnf` file.
The repository contains a `docker_db.cnf.example` example configuration file. The file must be with `RO` permissions or
Django will not use it to connect to the database.

Before the first run, the database must be created and populated with the schema. Run the migrations with the following
command:

```bash
python manage.py migrate
```

### Authentication

To access the administration interface at `/admin`, authentication is required.

By default, the project expects OIDC authentication to be used, which is configured through the
`/django/config/sso.json` file (see `sso.json.example`).

Alternatively, OIDC authentication can be disabled by setting the `OIDC_AUTH_DISABLE` environment variable to `1`. This
will make authentication fallback to Django's standard built-in username / password authentication.

You can create a superuser account through the Django admin interface using the following command:

```bash
python manage.py createsuperuser
```

### Kubernetes configuration

The connection to the cluster is done through the kubeconfig file, if run through the provided Dockerfile, the file must
be located in `/home/django/.kube/config`.

If the cloud provider itself is deployed also in Kubernetes, its deployment can use a service account with the
appropriate permissions to access the cluster. By default, it is assumed that the service account exists and a script
is executed to create the kubeconfig file from the service account's mounted secret.

````yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: visa-test
  name: alba-cloud-provider-deployment-test
  labels:
    app: visa
    component: alba-cloud-provider
    env: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: visa
      component: alba-cloud-provider
      env: test
  template:
    metadata:
      labels:
        app: visa
        component: alba-cloud-provider
        env: test
    spec:
      serviceAccountName: visa-acp-user-account
...
````

For security reasons, the service account should only have the necessary permissions to perform CRUD operations over
Deployments and StatefulSets, and strictly restricted to operate on specific namespaces.

Example limited cluster role:

````yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: visa-user-pods-clusterrole
rules:
  ...
  resources:
    - pods
  verbs:
    - create
    - delete
    - update
    - patch
    - watch
    - list
    - get
    - apiGroups:
        - apps
      resources:
        - deployments
      verbs:
        - create
        - delete
        - update
        - patch
        - watch
        - list
        - get
    - apiGroups:
        - apps
      resources:
        - statefulsets
      verbs:
        - create
        - delete
        - update
        - patch
        - watch
        - list
        - get
    - apiGroups:
        - ''
      resources:
        - configmaps
      verbs:
        - create
        - delete
        - update
        - patch
        - watch
        - list
        - get
    - apiGroups:
        - ''
      resources:
        - secrets
      verbs:
        - create
        - delete
        - update
        - patch
        - watch
        - list
        - get
    - apiGroups:
        - ''
      resources:
        - persistentvolumeclaims
      verbs:
        - create
        - delete
        - update
        - patch
        - watch
        - list
        - get
````

The cloud provider is configured to use different namespaces for different environments, and this is tied to the
settings file the cloud provider is using:

| Environment | Namespace        | Command                                                        |
|-------------|------------------|----------------------------------------------------------------|
| Test        | `visa-pods-prod` | `python manage.py runserver --settings=settings.settings_test` |
| Production  | `visa-pods-test` | `python manage.py runserver --settings=settings.settings_prod` |

Initially, VISA instances were created in the cluster as Deployments instead of StatefulSets. The decision was made to
switch to StatefulSets as to achieve a better control over the lifecycle of the instances. This can be changed back to
using desployments through the `settings.py` file, setting the variable `VISA_CLOUD_PROVIDER_USE_STATEFULSET` to
`False`.

### Connection with VISA

To connect VISA with the cloud provider, set the following environment variables in VISA's API server:

| Environment variable                 | Value                                 | Description                                                                       |
|--------------------------------------|---------------------------------------|-----------------------------------------------------------------------------------|
| `VISA_DEFAULT_CLOUD_PROVIDER_TYPE`   | `web`                                 | To switch from default's OpenStack provider.                                      |
| `VISA_DEFAULT_CLOUD_PROVIDER_NAME`   | `whatever`                            |                                                                                   |
| `VISA_CLOUD_WEB_PROVIDER_AUTH_TOKEN` |                                       | API token for the cloud provider (it can be obtained from the `/admin` interface. |
| `VISA_CLOUD_WEB_PROVIDER_URL`        | `https://k8s-cloud-provider/v1.21.14` | URL of cloud provider.**                                                          |
| `VISA_CLOUD_SERVER_NAME_PREFIX`      | `whatever as well`                    |                                                                                   |

**Note:** Add the `/v1.21.14` part of the URL to the version of the Kubernetes API you are using. Initially, before
switching to operators and CRDs, the idea was to support multiple Kubernetes versions through the same cloud provider.
The development of this feature has since stopped, but it's still required as part of the cloud provider's base URL.

### Configuring the cloud provider

#### Cluster limits (DB table)

Set the limits for the number of instances and resources that the cloud provider can use for provisioning VISA
instances.

| Name                    | Description                                         | Value | Unit      |
|-------------------------|-----------------------------------------------------|-------|-----------|
| MAX_TOTAL_RAM_ALLOWED   | Total amount of RAM allowed to use by the ACP       | 51200 | MiB       |
| MAX_INSTANCE_AMOUNT     | Total amount of instances allowed to use by the ACP | 15    | instances |
| MAX_TOTAL_CORES_ALLOWED | Total amount of cores allowed to use by the ACP     | 10    | cores     |

#### Instance services (DB table)

Satellite services that can be enabled for each instance (VISA print server, GUACD, Jupyter, etc.). These services are
tied to the flavours of the instances.

| name       | port | bind_address | protocol | sidecar_deployed | container_image                       | cpu_requests | memory_requests | cpu_limits | memory_limits | env_string                                                                                       | pull_secrets_name | pull_policy  | mount_pvc_storage | args                                                                                                                                                                                                                                                            | command | mount_tmp_dir | mount_scratch_dir |
|------------|------|--------------|----------|------------------|---------------------------------------|--------------|-----------------|------------|---------------|--------------------------------------------------------------------------------------------------|-------------------|--------------|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|---------------|-------------------|
| GUACD      | 4822 | 0.0.0.0      | TCP      | 1                | guacamole/guacd:1.5.5                 |              |                 |            |               |                                                                                                  |                   | IfNotPresent | 0                 |                                                                                                                                                                                                                                                                 |         | 0             | 0                 |
| VISA_PRINT | 8091 | 0.0.0.0      | TCP      | 1                | visa-print-service:latest             |              |                 |            |               | VISA_PRINT_SERVER_HOST=0.0.0.0                                                                   |                   | IfNotPresent | 0                 |                                                                                                                                                                                                                                                                 |         | 1             | 0                 |
| VISA_FS    | 8090 | 0.0.0.0      | TCP      | 1                | node-fs-api:latest                    |              |                 |            |               | HOME=/scratch/data-analysis¶NODE_FS_API_SERVER_HOST=0.0.0.0¶NODE_FS_API_MAX_FILE_UPLOAD_SIZE=0mb |                   | IfNotPresent | 0                 |                                                                                                                                                                                                                                                                 |         | 0             | 1                 |
| JUPYTER    | 8888 | 0.0.0.0      | TCP      | 1                | quay.io/jupyter/scipy-notebook:latest |              |                 |            |               |                                                                                                  |                   | IfNotPresent | 0                 | >¶mkdir -p $HOME/.visa-jupyter/ && echo "c.ServerApp.tornado_settings = {'xsrf_cookie_kwargs': {'path': '/'}}" > ${HOME}/.visa-jupyter/jupyter_cookie_override.py && jupyter lab --config=${HOME}/.visa-jupyter/jupyter_cookie_override.py --ip=0.0.0.0 --port= | sh -c   | 0             | 0                 |

#### Images (DB table)

| name                  | full_image_url  | size   | created_at              | home_template_path       | user_shell    | deleted | deleted_at |
|-----------------------|-----------------|--------|-------------------------|--------------------------|---------------|---------|------------|
| Debian 12 - Webx test | debian12:latest | 2222.0 | 2025-10-02 10:44:19.903 | /etc/visa_home_template/ | /usr/bin/bash | 0       |            |

## Contact and support

For any questions, contact the MIS section at the ALBA Synchrotron.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)