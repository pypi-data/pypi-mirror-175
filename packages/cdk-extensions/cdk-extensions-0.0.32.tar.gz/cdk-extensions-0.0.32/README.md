# Vibe.io

Vibe.io CDK extensions is a library of opinionated CDK constructs that will accelerate your project by laying a solid cloud foundation for your team to build on top of. Keeping your team focused on business value, while relying on a community to manage the common fundamentals like VPC, EKS, Cross Account Management, etc.

# Meet the Maintainers

[RightBrain Networks](https://www.rightbrainnetworks.com/) has spent the past decade forging cloud patterns, working with startups and enterprise clients to find the sweet spot where cloud infrastructure sits in a Software Development LifeCycle (SDLC). Identifying the right amount of self-service to unblock development, but with the right amount of support from operations to ensure we're building a secure, and auditable platform. We've found that the CDK construct library pattern lends itself in line with our goals, and provides a framework for adoption that enables us to share our work with the cloud operations community.

We are confident in our vision that Infrastructure as Code should follow an [Environments as Cattle approach](https://www.youtube.com/watch?v=z5XDAhyh9Z4). We've attempted to open source our patterns many times throughout the years, by way of CloudFormation repositories and troposphere initiatives and the like. CDK broke this wide open for us. We're able to develop and iterate on our patterns with true imperative code, that can be imported as a library by a consumer and used as necessary.

## If you need help, we're a community.

Use the GitHub issues to address problems

## If you have immediate concerns, email Joe

Email: joe@rightbrainetworks.com

![Joe Coleman](./images/joe.webp)

## Getting Started

### TypeScript

#### Installation

```shell
$ npm install cdk-extensions
```

### Python

#### Installation

```shell
$ pip install cdk-extensions
```

### Examples

#### AwsLoggingStack

Minimal deployable example creates the default logging strategy defined in AwsLoggingStack for Elastic Load Balancer, CloudFront, CloudTrail, VPC Flow Logs, S3 access logs, SES logs, and WAF logs. For each service, an S3 bucket is created and a Glue crawler to analyze and categorize the data and store the associated metadata in the AWS Glue Data Catalog. Default named queries have been defined for each AWS service. For more details on this and the other available stacks and constructs, consult the respective READMEs.

**TypeScript**

```TypeScript
import { AwsLoggingStack } from 'cdk-extensions/stacks';
```

```TypeScript
new AwsLoggingStack(this, 'AwsLoggingStack')
```

**Python**

```Python
from cdk_extensions.stacks import (
  AwsLoggingStack
)
```

```Python
aws_logging_stack = AwsLoggingStack(self, 'AwsLoggingStack')
```

#### Deploy

```shell
$ cdk deploy
```
