resource "oci_identity_compartment" "tf_compartment" {
  # Create this new compartment INSIDE root tenancy
  compartment_id = var.tenancy_ocid  
  name           = "terraform-compartment-v2"
  description    = "Compartment for Terraform resources"
  enable_delete  = true  # Allows to delete this later if needed
}