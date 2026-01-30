# Create the Block Volume (The Hard Drive)
resource "oci_core_volume" "db_volume" {
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  compartment_id      = oci_identity_compartment.tf_compartment.id
  display_name        = var.volume_display_name
  size_in_gbs         = var.volume_size # Size of the disk
}

# Attach the Volume to the Instance (The Cable)
resource "oci_core_volume_attachment" "db_volume_attach" {
  attachment_type = "paravirtualized" # Easier than iSCSI (auto-detected by Linux)
  instance_id     = oci_core_instance.db_server.id
  volume_id       = oci_core_volume.db_volume.id
}