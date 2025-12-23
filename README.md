# Cloud Endpoints DNS Module for Terraform

This module creates a [DNS record on the `.cloud.goog` domain](https://cloud.google.com/endpoints/docs/openapi/openapi-dns-configure) using Cloud Endpoints.

The endpoint service is bound to any given IP address and gives you a known DNS record in the form of: `NAME.endpoints.PROJECT.cloud.goog`

Some example use cases include:
- Obtaining a free DNS record for use with examples, demos or prototypes.
- Obtaining a free DNS record to use in conjunction with a SSL certificate.
- Obtaining a free DNS record to use with the Google Cloud Load Balancer to enable features like IAP which require a known DNS, and valid SSL certificate.
- Obtaining multiple canonical DNS records scoped within a project for a multi-tennant service deployment, like hosting Jupyter notebooks or Wordpress sites.
- Creating a programatic DNS record that can be used as a target for a CNAME record of a domain you already own but don't want to update very often.

## Compatibility
This module is meant for use with Terraform 0.13. If you haven't
[upgraded](https://www.terraform.io/upgrade-guides/0-13.html) and need a Terraform
0.12.x-compatible version of this module, the last released version
intended for Terraform 0.12.x is [v2.0.1](https://registry.terraform.io/modules/terraform-google-modules/-endpoints-dns/google/v2.0.1).

## Usage

```hcl
module "cloud-ep-dns" {
  source      = "terraform-google-modules/endpoints-dns/google"
  project     = "${data.google_client_config.current.project}"
  name        = "myservice"
  external_ip = "${google_compute_instance.default.network_interface.0.access_config.0.assigned_nat_ip}"
}
```

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| ensure\_undelete | Run gcloud command before creating cloud endpoint to force undelete of service endpoint. If endpoint has recently been deleted, it cannot be re-created without first undeleting it. | `bool` | `true` | no |
| external\_ip | External IP the endpoint will point to. | `any` | n/a | yes |
| name | Name of the cloud endpoints service. This will create a DNS record in the form of: NAME.endpoints.PROJECT.cloud.goog | `any` | n/a | yes |
| project | Project to create the Cloud Endpoint service in. If not given, the default provider is used. | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| config\_id | The rollout config ID for the endpoint service. |
| endpoint | The name of the DNS record conventional to the Cloud Endpoints format of: NAME.endpoints.PROJECT.cloud.goog. Not dependent on google\_endpoints\_service resource. |
| endpoint\_computed | The address of the cloud endpoint. This is computed from the google\_endpoints\_service resource and can be used to create dependencies between resources. |
| external\_ip | The value of the external IP the endpoint points to. |
| name | Name of the cloud endpoints service. |
| project | The project where the cloud endpoint was created. |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->