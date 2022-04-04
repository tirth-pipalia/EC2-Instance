import aws_cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct


class RmsInstanceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs, tags={"cost-center": "8998",
                                                              "department": "Information-technology",
                                                              "workload-name": "rms-webserver-prod"})

        vpc = ec2.Vpc.from_lookup(
            self,
            "VPCid",
            vpc_name="rms-prod-vpc",
        )

        securityGroup = ec2.SecurityGroup.from_lookup_by_id(self, "SecurityGroupIdForInstanceStack",
                                                            security_group_id="SecurityGroupID")

        iamInput = self.node.try_get_context("iamInput")
        iamRole = iam.Role.from_role_arn(
            self,
            "FromRoleARNId",
            role_arn=iamInput["roleARN"],
            mutable=iamInput["mutable"]
        )

        instanceInput = self.node.try_get_context("instanceInput")
        ec2Instance = ec2.Instance(
            self,
            "EC2ForAZ2ID",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass[instanceInput["instanceClass"]],
                                              ec2.InstanceSize[instanceInput["instanceSize"]]),
            machine_image=ec2.AmazonLinuxImage(),
            vpc=vpc,
            availability_zone=instanceInput["az"],
            instance_name=instanceInput["instanceName"],
            key_name=instanceInput["keyName"],
            role=iamRole,
            security_group=securityGroup,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
        )
