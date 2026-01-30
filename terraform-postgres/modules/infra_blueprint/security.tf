# Defines the "Security List" (Firewall). It contains specific rules allowing traffic on Port 22 (SSH) and Port 5432 (Postgres).

# Security List for Public Subnet
resource "oci_core_security_list" "public_sl" {
  compartment_id = oci_identity_compartment.tf_compartment.id
  vcn_id         = oci_core_vcn.main_vcn.id
  display_name   = "terraform-security-list"

  # EGRESS RULE (Outbound Traffic)
  egress_security_rules {
    destination = "0.0.0.0/0"  # Allow to all destinations. Allows the server to initiate connections to anywhere on the internet
    protocol    = "all"         # All protocols(TCP,UDP,ICMP, etc.)
  }

  # INGRESS RULE 1(Inbound Traffic): SSH Access
  # Allows SSH connections to manage the server remotely
  ingress_security_rules {
    protocol = "6"      # Protocol 6 = TCP. TCP is used for SSH and most other connections as its reliable.
    source   = "0.0.0.0/0" # Allow from any IP address
    tcp_options {
      min = 22 # SSH port. firewall rules often need to open a range of ports
      max = 22 # Only port 22
    }
  }

  # INGRESS RULE 2(Inbound Traffic): PostgreSQL Database Access
  ingress_security_rules {
    protocol = "6"     # Protocol 6 = TCP
    source   = "0.0.0.0/0" # Allow from any IP address
    tcp_options {
      min = 5432  
      max = 5432  
    }
  }

  # Allow Ping (ICMP)
  ingress_security_rules {
    protocol = "1"  # Protocol 1 is ICMP
    source   = "0.0.0.0/0"
  }
}



