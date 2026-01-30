# contains the actual values for the variables defined in variables.tf
# A .tfvars file is strictly for assigning values. It cannot define new resources or new variables.
tenancy_ocid     = "ocid1.tenancy.oc1..aaaaaaaauyovd3mtxmxpx7md6gdtyohwe6p3b36zayw34o2trktvdon7f6wq"
user_ocid        = "ocid1.user.oc1..aaaaaaaauj7ot4m5po7tbgphc2ilyhwmtzub3fotevmxeykpfvb7sqi2hjfq"
private_key_path = "/home/ravindu-rashmika/.oci/oci_api_key.pem"
fingerprint      = "26:a1:69:3c:06:b9:f4:ed:88:af:90:05:fd:d2:6c:0b"
region           = "ap-singapore-1"
compartment_ocid = "ocid1.tenancy.oc1..aaaaaaaauyovd3mtxmxpx7md6gdtyohwe6p3b36zayw34o2trktvdon7f6wq"



vm_display_name = "terraform-test-vm-v2"
vm_shape        = "VM.Standard.E5.Flex"
vm_ocpus        = 1
vm_memory       = 4

volume_display_name = "terraform-data-volume"
volume_size         = 50

ssh_key_path = "~/.ssh/id_rsa_terraform.pub"