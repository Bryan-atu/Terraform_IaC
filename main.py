#!/usr/bin/env python
from constructs import Construct
from cdktf import App, NamedRemoteWorkspace, TerraformStack, TerraformOutput, RemoteBackend, TerraformVariable
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Define a variable for the region
        region_var = TerraformVariable(self, "region", default="eu-west-1", description="AWS region to deploy resources")

        # Define a variable for the AMI ID
        ami_var = TerraformVariable(self, "ami_id", 
                                    default="ami-008d05461f83df5b1", 
                                    description="AMI ID to use for the EC2 instance")
        

        AwsProvider(self, "AWS", region=region_var.value)


        # Define EC2 instance
        instance = Instance(self, "compute",
                            ami=ami_var.to_string(),
                            instance_type="t2.micro",
                            tags={
                                "Name": "TF2",
                                "Environment": "Development",
                                "Owner": "Dev Team"
                            })

        # Output IPs
        TerraformOutput(self, "public_ip", value=instance.public_ip)

        TerraformOutput(self, "instance_id", value=instance.id)

app = App()
stack = MyStack(app, "aws_instance")

RemoteBackend(stack,
              hostname='app.terraform.io',
              organization='IaC_Terraform_BG',
              workspaces=NamedRemoteWorkspace('IaC_Tf2')
              )

# Synthesize the application
app.synth()