# Defines the Virtual Cloud Network (VCN), the Internet Gateway, and the Public Subnet.

# Virtual Cloud Network (VCN)
resource "oci_core_vcn" "main_vcn" {
  cidr_block     = "10.0.0.0/16"       # VCN range
  compartment_id = oci_identity_compartment.tf_compartment.id # Compartment value take from compartment.tf. Where VCN will be created
  display_name   = "terraform-vcn"  
  dns_label      = "tfvcn"         # DNS label for internal hostname resolution
}

# Internet Gateway
resource "oci_core_internet_gateway" "main_ig" {
  compartment_id = oci_identity_compartment.tf_compartment.id          # Same compartment as VCN
  vcn_id         = oci_core_vcn.main_vcn.id      # Attach to our VCN
  display_name   = "terraform-internet-gateway" 
}

# Route Table
# Defines routing rules that control how traffic flows in and out of subnets
resource "oci_core_route_table" "main_rt" {
  compartment_id = oci_identity_compartment.tf_compartment.id
  vcn_id         = oci_core_vcn.main_vcn.id
  display_name   = "terraform-route-table"

  # Route Rule: Send all internet-bound traffic through the Internet Gateway
  route_rules {
    destination       = "0.0.0.0/0"                       
    destination_type  = "CIDR_BLOCK"          # Using CIDR notation
    network_entity_id = oci_core_internet_gateway.main_ig.id  # Route through our internet gateway
  }
}

# Public Subnet - where our compute instance will be placed
resource "oci_core_subnet" "public_subnet" {
  cidr_block        = "10.0.1.0/24"          
  compartment_id    = oci_identity_compartment.tf_compartment.id    # Same compartment
  vcn_id            = oci_core_vcn.main_vcn.id # Must belong to VCN
  display_name      = "terraform-public-subnet" 
  dns_label         = "public"                # Used for internal hostnames
  security_list_ids = [oci_core_security_list.public_sl.id] # Attach security rules
  # Link this subnet to the Route Table - enables internet routing
  route_table_id = oci_core_route_table.main_rt.id
}
