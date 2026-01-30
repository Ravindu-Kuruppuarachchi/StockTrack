# COMPUTE INSTANCE

# This creates a virtual machine in Oracle Cloud Infrastructure
resource "oci_core_instance" "db_server" {
  # PLACEMENT CONFIGURATION
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name  # Use first available AD
  compartment_id      = oci_identity_compartment.tf_compartment.id # compartment taken from compartment.tf
  display_name        = var.vm_display_name   # Name shown in OCI console

  # Hardware Configuration - Defines CPU and memory resources for the VM
  shape = var.vm_shape  
  shape_config {
    ocpus         = var.vm_ocpus  # 1 Oracle CPU Unit - equivalent to 2 vCPUs
    memory_in_gbs = var.vm_memory  # 4GB RAM
  }

  # Network Configuration - Connects the instance to our subnet and assigns a public IP
  
  create_vnic_details {
    subnet_id        = oci_core_subnet.public_subnet.id  # Place in public subnet
    assign_public_ip = true  # Assign a public IP for internet access
  }

  # Operating System Image - Specifies which OS to install on the instance
  source_details {
    source_type = "image"  # Using a pre-built image
    source_id   = data.oci_core_images.ubuntu_latest.images[0].id  # Latest Ubuntu 22.04 image
  }

  # SSH KEY INJECTION
  # The key is injected into ~/.ssh/authorized_keys for the default user
  metadata = {
    ssh_authorized_keys = file(var.ssh_key_path)  # Read public key from local file
  }
}

# Output: Public IP Address
# Displays the public IP address of the instance for SSH and database connections
output "server_public_ip" {
  value = oci_core_instance.db_server.public_ip
}
