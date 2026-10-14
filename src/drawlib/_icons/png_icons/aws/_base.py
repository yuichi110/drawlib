# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""AWS icon provider configuration and writer."""

from __future__ import annotations

from drawlib._icons.png_icons._base import PngIconProvider

AWS_ALIASES: dict[str, str] = {
    "acm": "certificate_manager",
    "alb": "elastic_load_balancing",
    "apigw": "api_gateway",
    "cdk": "cloud_development_kit",
    "cli": "command_line_interface",
    "cloudwatch_logs": "cloudwatch",
    "cognito_id": "cognito",
    "dms": "database_migration_service",
    "ebs": "elastic_block_store",
    "ecr": "elastic_container_registry",
    "ecs": "elastic_container_service",
    "eks": "elastic_kubernetes_service",
    "elastic_file_system": "efs",
    "elb": "elastic_load_balancing",
    "eventbridge_bus": "eventbridge",
    "flink": "managed_service_for_apache_flink",
    "iam": "identity_and_access_management",
    "kms": "key_management_service",
    "lambda_function": "aws_lambda",
    "msk": "managed_streaming_for_apache_kafka",
    "nlb": "elastic_load_balancing",
    "opensearch": "opensearch_service",
    "prometheus": "managed_service_for_prometheus",
    "ram": "resource_access_manager",
    "route53": "route_53",
    "s3": "simple_storage_service",
    "s3_glacier": "simple_storage_service_glacier",
    "ses": "simple_email_service",
    "sns": "simple_notification_service",
    "sqs": "simple_queue_service",
    "step_functions_workflow": "step_functions",
    "vpc": "virtual_private_cloud",
}

AWS_PROVIDER = PngIconProvider(
    name="aws",
    package_name="icon_aws",
    asset_subdir="icons/aws",
    aliases=AWS_ALIASES,
)

_write = AWS_PROVIDER.write
