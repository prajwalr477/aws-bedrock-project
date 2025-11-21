provider "aws" {
  region  = "us-east-1"
  profile = "udacity"
}

module "bedrock_kb" {
  source = "../modules/bedrock_kb" 

  knowledge_base_name        = "my-bedrock-kb"
  knowledge_base_description = "Knowledge base connected to Aurora Serverless database"

  aurora_arn               = "arn:aws:rds:us-east-1:403578927512:cluster:my-aurora-serverless"
  aurora_db_name           = "myapp"
  aurora_endpoint          = "my-aurora-serverless.cluster-c80hxzddy3tt.us-east-1.rds.amazonaws.com"
  aurora_table_name        = "bedrock_integration.bedrock_kb"
  aurora_primary_key_field = "id"
  aurora_metadata_field    = "metadata"
  aurora_text_field        = "chunks"
  aurora_verctor_field     = "embedding"
  aurora_username          = "dbadmin"
  aurora_secret_arn        = "arn:aws:secretsmanager:us-east-1:403578927512:secret:my-aurora-serverless-p3cusN"
  s3_bucket_arn            = "arn:aws:s3:::bedrock-kb-403578927512"
}
