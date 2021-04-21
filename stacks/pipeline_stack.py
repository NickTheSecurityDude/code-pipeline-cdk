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

  def __init__(self, scope: core.Construct, construct_id: str, env, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # get acct id for policies
    acct_id=env['account']

    # create a bucket
    my_bucket = s3.Bucket(self,"Bucket")

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
        bucket_key="sg1.yaml",
        output=my_s3_artifact
      )
    )

    #s3_output=pipeline.Artifact()

    # add 2nd stage
    # approval_stage = my_pipeline.add_stage(stage_name="Approval")
    # approval_stage.add_action(
    #  pipeline_actions.ManualApprovalAction(
    #    action_name="Manual-Approval"
    #  )
    #)
     
    # create IRole
    my_remote_role=iam.Role.from_role_arn(self,"Role","arn:aws:iam::123456789012:role/cf_x_acct_role")

    # add nth stage
    deploy_stage = my_pipeline.add_stage(stage_name="Deploy")
    deploy_stage.add_action(
      pipeline_actions.CloudFormationCreateUpdateStackAction(
        action_name="Deploy",
        admin_permissions=True,
        stack_name="my-stack",
        template_path=my_s3_artifact.at_path(
          "sg1.yaml"
        ),
        #deployment_role=my_remote_role
        role=my_remote_role
      )
    )


