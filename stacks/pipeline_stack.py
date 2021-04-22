##############################################################
#
# pipeline_stack.py
#
# Resources:
#
##############################################################

from aws_cdk import (
  aws_codepipeline as pipeline,
  aws_codepipeline_actions as pipeline_actions,
  aws_s3 as s3,
  aws_iam as iam,
  core
)

class PipelineStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id,**kwargs)

    # get acct id for policies
    #acct_id=env['account']
    
    ## the account cloudformation will deploy to
    x_acct="222"
    x_acct_arn="arn:aws:iam::"+x_acct+":role/cf_x_acct_role"

    # create a bucket
    my_bucket = s3.Bucket(self,"Source Bucket",
      versioned=True
    )
 
    # create the pipeline
    my_pipeline = pipeline.Pipeline(self, "My Pipeline")

    # add a stage
    source_stage = my_pipeline.add_stage(stage_name="Source")

    # s3 output artifact
    my_s3_artifact=pipeline.Artifact()

    # add a source action to the stage
    source_stage.add_action(
      pipeline_actions.S3SourceAction(
        action_name="Source",
        bucket=my_bucket,
        bucket_key="sg1.zip",
        output=my_s3_artifact
      )
    )

    # create IRole
    my_remote_role=iam.Role.from_role_arn(self,"Role",x_acct_arn)

    # add nth stage
    deploy_stage = my_pipeline.add_stage(stage_name="Deploy")
    deploy_stage.add_action(
      pipeline_actions.CloudFormationCreateUpdateStackAction(
        action_name="Deploy",
        account=x_acct,
        admin_permissions=True,
        stack_name="my-stack",
        template_path=my_s3_artifact.at_path(
          "sg1.yaml"
        ),
        deployment_role=my_remote_role
      )
    )



