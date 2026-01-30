# defines the inputs your project expects,
# These variables allow you to customize your deployment without changing code

# Tenancy OCID - The root compartment of your Oracle Cloud account
variable "tenancy_ocid" {
  description = "OCID of tenancy"
  type        = string
}

# User OCID - Identifies the specific user making API calls to OCI
variable "user_ocid" {
  description = "OCID of user"
  type        = string
}

# Private Key Path - Required for API authentication to OCI
variable "private_key_path" {
  description = "Path to private OCI API key on laptop"
  type        = string
}

# Fingerprint - Used to verify the authenticity of your private key
variable "fingerprint" {
  description = "Fingerprint for the private key"
  type        = string
}

# Region - The geographical location where your resources will be deployed
variable "region" {
  description = " The OCI region (e.g., ap-mumbai-1 or us-ashburn-1)"
  type        = string
  default     = "ap-singapore-1"  # Default region if not specified
}

# Compartment OCID - The logical container where all resources will be organized
variable "compartment_ocid" {
  description = "OCID of the compartment where resources will be created"
  type        = string
}


# Compute Variables
variable "vm_display_name" {
  description = "Name of the VM"
  type        = string
}

variable "vm_shape" {
  description = "The hardware shape (e.g., VM.Standard.E5.Flex)"
  type        = string
}

variable "vm_ocpus" {
  description = "Number of OCPUs"
  type        = number
}

variable "vm_memory" {
  description = "Amount of RAM in GB"
  type        = number
}



# Storage Variables
variable "volume_size" {
  description = "Size of the extra disk in GB"
  type        = number
}

variable "volume_display_name" {
  description = "Name of the block volume"
  type        = string
}


# SSH Key Path - Path to the public SSH key for VM access
variable "ssh_key_path" {
  description = "Path to the public SSH key"
  type        = string
}