# Drawlib AWS Icons Guidelines (`lib-icons-aws`)

API specification and complete 80-service catalog for `drawlib.icons.aws` (`AwsIcon`, `aws_icon`). See `lib-icons-overview` for cross-tier icon rules and `lib-diagrams-architecture` for `ArchitectureDiagram`.

---

## 1. Overview & API Signatures

`drawlib.icons.aws` provides **80 official Amazon Web Services (AWS) architecture icons** rendered from normalized `512×512` RGBA PNG assets (`icon_aws` archive).

```python
from drawlib.diagrams.architecture import AwsIcon, Node, NodeGroup
from drawlib.icons import aws, aws_icon
from drawlib.styles import Styles
from drawlib.types import Style

# 1. Direct function call (center-anchored at (cx, cy); style is required keyword-only)
def <service_name>(
    xy: tuple[float, float],
    width: float,
    *,
    style: Style,
    variant: str = "default",
) -> None: ...

# 2. Dynamic string/Enum dispatcher
def aws_icon(
    xy: tuple[float, float],
    width: float,
    name: str | AwsIcon,
    *,
    style: Style,
    variant: str = "default",
) -> None: ...
```

- **Python Keyword Avoidance (`aws_lambda`)**: Because `lambda` is a reserved keyword in Python, AWS Lambda is named **`aws.aws_lambda`** (`AwsIcon.AWS_LAMBDA`).
- **Center Anchor & Required `style`**: Anchored at `xy=(cx, cy)` with `1:1` square aspect ratio; `*, style: Style` is mandatory.

```drawlib code=fold align=center file=icons_aws_rules_showcase.png caption="AWS Serverless & Event-Driven Topology Using ArchitectureDiagram and AwsIcon"
from drawlib.canvas import save, setup
from drawlib.diagrams.architecture import ArchitectureDiagram, AwsIcon, Node, NodeGroup
from drawlib.styles import Styles

setup(width=140, height=58)

d = ArchitectureDiagram(
    node_style=Styles.Primary,
    node_text_style=Styles.DarkBold.patch(text_size=10.0),
    edge_style=Styles.DarkBold,
    edge_text_style=Styles.DarkBold.patch(text_size=10.0),
    node_card_style=Styles.Neutral,
)

cf = d.add(
    Node("Amazon\nCloudFront", width=24, height=18, icon=AwsIcon.CLOUDFRONT, icon_size=7.5, card_style=Styles.PrimaryNeutral),
    xy=(6, 18),
)
vpc = d.add(
    NodeGroup(title="AWS Production Region / VPC", padding=4.5),
    xy=(42, 4),
)
fn = vpc.add(Node("AWS Lambda", width=24, height=18, icon=AwsIcon.AWS_LAMBDA, icon_size=7.5, card_style=Styles.PrimaryNeutral), xy=(14, 14))
db = vpc.add(Node("Amazon\nDynamoDB", width=24, height=18, icon=AwsIcon.DYNAMODB, icon_size=7.5, card_style=Styles.SecondaryNeutral), xy=(54, 14))

d.connect(cf, fn, label="HTTPS", padding=1.5)
d.connect(fn, db, label="PutItem", padding=1.5)
d.draw(xy=(4, 4))
save()
```

---

## 2. Complete Canonical 80 AWS Icons Reference (`aws.*` & `AwsIcon.*`)

Every service below is callable as `aws.<name>(xy, width, style=...)` and `AwsIcon.<NAME>`:

| AWS Service Category | Count | Canonical Function Names (`aws.*`) | `AwsIcon` Enum Members |
| :--- | :---: | :--- | :--- |
| **1. Compute & Serverless** | 8 | `app_runner`, `auto_scaling`, `batch`, `ec2`, `elastic_beanstalk`, `aws_lambda`, `lightsail`, `outposts` | `APP_RUNNER`, `AUTO_SCALING`, `BATCH`, `EC2`, `ELASTIC_BEANSTALK`, `AWS_LAMBDA`, `LIGHTSAIL`, `OUTPOSTS` |
| **2. Containers & Orchestration** | 4 | `ecr`, `ecs`, `eks`, `fargate` | `ECR`, `ECS`, `EKS`, `FARGATE` |
| **3. Storage, Backup & Migration** | 7 | `backup`, `datasync`, `ebs`, `efs`, `fsx`, `s3`, `s3_glacier`, `snowball`, `storage_gateway` | `BACKUP`, `DATASYNC`, `EBS`, `EFS`, `FSX`, `S3`, `S3_GLACIER`, `SNOWBALL`, `STORAGE_GATEWAY` |
| **4. Databases & Caching** | 8 | `aurora`, `documentdb`, `dynamodb`, `elasticache`, `keyspaces`, `memorydb`, `neptune`, `rds`, `timestream` | `AURORA`, `DOCUMENTDB`, `DYNAMODB`, `ELASTICACHE`, `KEYSPACES`, `MEMORYDB`, `NEPTUNE`, `RDS`, `TIMESTREAM` |
| **5. Networking & Content Delivery** | 11 | `api_gateway`, `app_mesh`, `cloud_map`, `cloudfront`, `direct_connect`, `elastic_load_balancing`, `global_accelerator`, `nat_gateway`, `privatelink`, `route_53`, `transit_gateway`, `vpc`, `vpn` | `API_GATEWAY`, `APP_MESH`, `CLOUD_MAP`, `CLOUDFRONT`, `DIRECT_CONNECT`, `ELASTIC_LOAD_BALANCING`, `GLOBAL_ACCELERATOR`, `NAT_GATEWAY`, `PRIVATELINK`, `ROUTE_53`, `TRANSIT_GATEWAY`, `VPC`, `VPN` |
| **6. Analytics, Streaming & Big Data** | 9 | `athena`, `clean_rooms`, `data_exchange`, `emr`, `glue`, `kinesis`, `lake_formation`, `msk`, `opensearch_service`, `quicksight`, `redshift` | `ATHENA`, `CLEAN_ROOMS`, `DATA_EXCHANGE`, `EMR`, `GLUE`, `KINESIS`, `LAKE_FORMATION`, `MSK`, `OPENSEARCH_SERVICE`, `QUICKSIGHT`, `REDSHIFT` |
| **7. Application Integration & Messaging** | 5 | `appsync`, `eventbridge`, `mq`, `sns`, `sqs`, `step_functions` | `APPSYNC`, `EVENTBRIDGE`, `MQ`, `SNS`, `SQS`, `STEP_FUNCTIONS` |
| **8. Security, Identity & Compliance** | 10 | `artifact`, `certificate_manager`, `cognito`, `guardduty`, `iam`, `inspector`, `kms`, `macie`, `network_firewall`, `secrets_manager`, `security_hub`, `shield`, `waf` | `ARTIFACT`, `CERTIFICATE_MANAGER`, `COGNITO`, `GUARDDUTY`, `IAM`, `INSPECTOR`, `KMS`, `MACIE`, `NETWORK_FIREWALL`, `SECRETS_MANAGER`, `SECURITY_HUB`, `SHIELD`, `WAF` |
| **9. AI & Machine Learning** | 6 | `bedrock`, `comprehend`, `kendra`, `lex`, `polly`, `q`, `rekognition`, `sagemaker`, `textract`, `transcribe`, `translate` | `BEDROCK`, `COMPREHEND`, `KENDRA`, `LEX`, `POLLY`, `Q`, `REKOGNITION`, `SAGEMAKER`, `TEXTRACT`, `TRANSCRIBE`, `TRANSLATE` |
| **10. Developer Tools, Management & IoT** | 12 | `amplify`, `cloudformation`, `cloudshell`, `cloudtrail`, `cloudwatch`, `codeartifact`, `codebuild`, `codecommit`, `codedeploy`, `codepipeline`, `config`, `control_tower`, `iot_core`, `organizations`, `systems_manager`, `trusted_advisor`, `well_architected_tool`, `x_ray` | `AMPLIFY`, `CLOUDFORMATION`, `CLOUDSHELL`, `CLOUDTRAIL`, `CLOUDWATCH`, `CODEARTIFACT`, `CODEBUILD`, `CODECOMMIT`, `CODEDEPLOY`, `CODEPIPELINE`, `CONFIG`, `CONTROL_TOWER`, `IOT_CORE`, `ORGANIZATIONS`, `SYSTEMS_MANAGER`, `TRUSTED_ADVISOR`, `WELL_ARCHITECTED_TOOL`, `X_RAY` |
