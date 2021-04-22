# code-pipeline-cdk

- enter your main account number in app.py
- ALSO enter your deploying to account number in stacks/pipeline_stack.py
- use a trust policy for the x-acct role like this: x-acct-trust-policy.json
- deploy the "support stack" first
- then deploy the pipeline stack with the --exclusively flag
- upload sg1.zip to the s3 source bucket
