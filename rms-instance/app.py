#!/usr/bin/env python3
import os

import aws_cdk as cdk
from rms_instance.rms_instance_stack import RmsInstanceStack


app = cdk.App()
env_ME = cdk.Environment(account="12_digit_account_no", region="me-south-1")
RmsInstanceStack(app, "RmsInstanceStack", env=env_ME)

app.synth()
