#!/usr/bin/env python3

# Import specific constructs groups from aws_cdk according to our needs
from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    App, RemovalPolicy, Stack
)


# Create class inheriting from Stack to make it possible to transform whole class to aws template (at the end of code)
class RDSStack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # Create Virtual Private Cloud to contain database
        # as parameters for every construct we use self and specific name of object (sometimes called id)
        vpc = ec2.Vpc(self, "VPC")

        # Create RDS DatabaseInstance construct and define all variables inside. Pycharm will suggest
        # parameters and conduct code verification as aws_cdk is python library

        rds.DatabaseInstance(
            self, "RDS",
            database_name="db1",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_3
            ),

            # point previously created vpc to assure connection (RDS cluster will be part of VPC)
            # if left empty the liblary will create new, default VPC
            vpc=vpc,
            port=5432,

            # Determine class and size of database cluster check for details:
            # https://aws.amazon.com/ec2/instance-types/
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.MEMORY4,
                ec2.InstanceSize.LARGE,
            ),

            # determine what will happen when command to destroy the stack in this case we make it possible
            # to destroy database alongside with the rest of stack (strongly not recommended for production !)
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        ),


# point the highest order structure with App()
app = App()

# Place the construct we have created RDSStack as a part of app
RDSStack(app, "RDSStack")

# Appoint function creating CloudFormation templates from our construct
app.synth()
