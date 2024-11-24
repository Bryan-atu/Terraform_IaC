#!/usr/bin/env python
from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput, RemoteBackend, TerraformVariable
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance

class AwsVariables:
    def __init__(self, stack: TerraformStack):
        # Define Terraform variables for region and AMI ID
        self.region_var = TerraformVariable(stack, "region", default="eu-west-1", description="AWS region to deploy resources")
        self.ami_var = TerraformVariable(stack, "ami_id", default="ami-008d05461f83df5b1", description="AMI ID to use for the EC2 instance")

    def get_region(self):
        return self.region_var  # Return the variable references

    def get_ami(self):
        return self.ami_var  

class AwsProviderConfig:
    def __init__(self, stack: TerraformStack, region: TerraformVariable):
        AwsProvider(stack, "AWS", region=region.to_string())

class Ec2Instance:
    def __init__(self, stack: TerraformStack, ami: TerraformVariable, instance_type: str = "t2.micro", tags: dict = None):
        # Create the EC2 instance using the ami variable
        self.instance = Instance(stack, "compute",
                                  ami=ami.to_string(),
                                  instance_type=instance_type,
                                  tags=tags or {
                                      "Name": "TF2",
                                      "Environment": "Development",
                                      "Owner": "Dev Team"
                                  })

    def get_instance(self):
        return self.instance

class Outputs:
    def __init__(self, stack: TerraformStack, instance: Instance):
        TerraformOutput(stack, "public_ip", value=instance.public_ip)
        TerraformOutput(stack, "instance_id", value=instance.id)

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Initialize variables
        aws_vars = AwsVariables(self)
        
        # Initialize AWS provider with the region variable
        AwsProviderConfig(self, aws_vars.get_region()) 

        # Create EC2 instance
        instance = Ec2Instance(self, aws_vars.get_ami())

        # Create outputs
        Outputs(self, instance.get_instance())

app = App()
stack = MyStack(app, "aws_instance")

# Configure remote backend
RemoteBackend(stack,
              hostname='app.terraform.io',
              organization='IaC_Terraform_BG',
              workspaces=NamedRemoteWorkspace('IaC_Tf2'))

app.synth()