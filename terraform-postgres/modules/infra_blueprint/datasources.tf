# This file doesn't create anything; it looks things up. It asks Oracle: "What is the ID of the latest Ubuntu 22.04 image?"
data "oci_identity_availability_domains" "ads" {
  compartment_id = oci_identity_compartment.tf_compartment.id  # Query at tenancy level to see all ADs
}

# Automatically finds the latest Ubuntu 22.04 image for our VM shape
# mage IDs change frequently as Oracle releases patches. Instead of hardcoding an ID that might expire,
# this file dynamically finds the correct, current ID every time we run Terraform.
data "oci_core_images" "ubuntu_latest" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Canonical Ubuntu"     # Filter for Ubuntu images
  operating_system_version = "22.04"                # Ubuntu version
  shape                    =  var.vm_shape # Must match the shape in compute.tf
  sort_by                  = "TIMECREATED"          # Sort by creation time
  sort_order               = "DESC"                 # Newest first in descending order
}
