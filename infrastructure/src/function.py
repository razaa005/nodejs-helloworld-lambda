import sys
from troposphere import GetAtt, Sub
from troposphere import Parameter, Ref, Template
from troposphere.iam import PolicyType
from troposphere.iam import Role
from troposphere.awslambda import Alias
from troposphere.awslambda import Function, Code
from troposphere.logs import LogGroup


t = Template()

LambdaEnv = t.add_parameter(Parameter(
    "LambdaEnv",
    Default="test",
    Description="Environment this lambda represents - used for alias name",
    Type="String",
))

LambdaHandler = t.add_parameter(Parameter(
    "LambdaHandler",
    Default="index.handler",
    Description="The name of the function (within your source code) that Lambda calls to start running your code.",
    Type="String",
))

LambdaMemorySize = t.add_parameter(Parameter(
    "LambdaMemorySize",
    Description="The amount of memory, in MB, that is allocated to your Lambda function.",
    Default="128",
    Type="Number",
))

LambdaTimeout = t.add_parameter(Parameter(
    "LambdaTimeout",
    Default="15",
    Description="The function execution time (in seconds) after which Lambda terminates the function. ",
    Type="Number",
))

LambdaFunctionName = t.add_parameter(Parameter(
    "LambdaFunctionName",
    Type="String",
    AllowedPattern="^[a-zA-Z0-9]+[a-zA-Z0-9-]+[a-zA-Z0-9]+$",
    Default="simple-lambdaFunction",
))

LambdaRuntime = t.add_parameter(Parameter(
    "LambdaRuntime",
    Type="String",
    AllowedValues=["nodejs18.x", "nodejs20.x"],
    Default="nodejs20.x",
))

FunctionPolicy = t.add_resource(PolicyType(
    "FunctionPolicy",
    PolicyDocument={"Id": "FunctionPolicy", "Statement": [{"Action": [
        "logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], "Effect": "Allow", "Resource": ["arn:aws:logs:*:*:*"]}], "Version": "2012-10-17"},
    PolicyName="function-policy",
    Roles=[Ref("FunctionRole")],
))

FunctionRole = t.add_resource(Role(
    "FunctionRole",
    AssumeRolePolicyDocument={"Statement": [{"Action": [
        "sts:AssumeRole"], "Effect": "Allow", "Principal": {"Service": ["lambda.amazonaws.com"]}}]},
))

LambdaAlias = t.add_resource(Alias(
    "LambdaAlias",
    Description="Cosmos Alias",
    FunctionName=Ref("LambdaFunction"),
    FunctionVersion="$LATEST",
    Name=Ref(LambdaEnv),
))

LambdaFunction = t.add_resource(Function(
    "LambdaFunction",
    FunctionName=Ref(LambdaFunctionName),
    Code=Code(ZipFile="exports.handler = function(event,context){}"),
    Description="A function template",
    Handler=Ref(LambdaHandler),
    MemorySize=Ref(LambdaMemorySize),
    Role=GetAtt(FunctionRole, "Arn"),
    Runtime=Ref(LambdaRuntime),
    Timeout=Ref(LambdaTimeout),
))

lambdaLogGroup = t.add_resource(LogGroup(
    "lambdaLogGroup",
    LogGroupName=Sub("/aws/lambda/${LambdaFunctionName}"),
    RetentionInDays=90,
))

template = t.to_json(indent=4, sort_keys=False)

if len(sys.argv) > 1:
    open(sys.argv[1], "w").write(template + "\n")
else:
    print(template)
