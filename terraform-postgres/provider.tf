# This file configures the "Provider" (plugin) that allows Terraform to speak the specific API language of Oracle Cloud
terraform {
  required_providers {
    #Oracle Cloud Infrastructure provider
    oci = {
      source  = "oracle/oci"  # Official Oracle provider from the Terraform registry
      version = ">= 5.0.0"  # Minimum version 5.0.0 to ensure compatibility
    }
  }
}

#Configures authentication and connection details
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid      # OCI tenancy identifier(root compartment) 
  user_ocid        = var.user_ocid         # OCI user identifier
  private_key_path = var.private_key_path  # Path to private API key file
  fingerprint      = var.fingerprint       # Fingerprint of API key for authentication
  region           = var.region            # OCI region where resources will be created
}
