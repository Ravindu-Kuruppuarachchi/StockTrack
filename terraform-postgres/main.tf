# This block calls the code sitting in the sub-folder
module "my_project_infrastructure" {
  # TWhere is the blueprint?
    source = "./modules/infra_blueprint"

    # Passing data from root down to the module
    tenancy_ocid     = var.tenancy_ocid
    user_ocid        = var.user_ocid
    private_key_path = var.private_key_path
    fingerprint      = var.fingerprint
    region           = var.region
    compartment_ocid = var.compartment_ocid

    vm_display_name = var.vm_display_name
    vm_shape        = var.vm_shape
    vm_ocpus        = var.vm_ocpus
    vm_memory       = var.vm_memory

    volume_display_name = var.volume_display_name
    volume_size         = var.volume_size 

    ssh_key_path = var.ssh_key_path
}