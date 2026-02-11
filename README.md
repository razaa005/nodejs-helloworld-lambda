### Overview
A sample to be used as a starting point for Node packages deployed via Cosmos.


### Infrastructure
The Cloudformation templates are defined in Python using troposphere in `infrastructure/src/*.py`.

To rebuild your `.json` templates, modify the relevant `.py` file and run:
```
$ cd infrastructure
$ make all
```
Then use the templates under `infrastructure/templates/*.json` and build the stacks in your corresponding accounts.


### Package
There are Makefile targets in the root directory to test, build and release your package via Cosmos.

# Test and build runtime versions
Test and build targets are defined in the Makefile, both use Node containers to ensure a consistent environment with your Lambda. It's important here that you use the same version that your Lambda is configured for.

All make targets accept a `NODE_VERSION` variable. It's set to `20` as default, if you are using a different version then you can (and should) change this like so:

```
$ NODE_VERSION={LAMBDA_NODE_VERSION} make in_container/test
```

# Cosmos component creation
Cosmos release requires a lambda component in cosmos to be able to create a release. To do so, open the relevant aws project in cosmos and click create under the AWS Lambdas section. 

# Updating parameters
There are three different parameters which you will need to update. Either by passing in as arguments to the make target or updating the Makefile.

COMPONENT_NAME - The name of your cosmos lambda component

CERT - Location of your .crt file

KEY - Location of your .key file

# Production build and release
To build and release your package via Cosmos in one fell swoop:

```
$ CERT=~/.certee/client.crt KEY=~/.certee/client.key COMPONENT_NAME=hello_world_lambda PROJECT_PATH=developer make in_container/build_and_release
```

This will run through all of the below make targets, and in sequence:
    - Clean up any leftover build/test directories from previous runs
    - [In a node container] Generate your build directory with all src code and dependencies
    - Zip up your build directory (excluding test files)
    - Release via Cosmos

If you would prefer to run these steps individually then follow the stages below.


# Test
To run your tests in a node:20 container, run:
```
$ make in_container/test
```


# Build
To generate a build directory in a node:20 container, run:
```
$ make in_container/build
```
At the end of this you will have a `BUILD` directory which includes all of your dependencies as well as the contents of your `src` directory. This setup ensures compatability with AWS Inspector - if you're thinking of changing this step then please read the [AWS Inspector Compatibility docs]('https://confluence.dev.bbc.co.uk/display/platform/AWS+Inspector+Compatibility') first!

To zip your package ready for upload, run:
```
$ make zip
```
This will create a `package.zip` file inside of the `BUILD` directory, excluding your `*.test.js` files.


# Release
To release the Lambda package, make sure the `package.zip` exists in the `BUILD` directory and run:
```
$ make release
```

This will build the package running the target above and then use the `cosmos-release` tool to generate a version, upload the package in the lambda-repository and post the release metadata to Cosmos.

# Deploying to an environment via Cosmos
At this stage there will be a latest release available from the component page in cosmos. To be able to deploy this, first create a stack by copying across the json containing the template found at: nodejs-helloworld-lambda/infrastructure/templates/function.json, and update the accountId and stack-suffix values appropiately. When the stack status shows "CREATE_COMPLETE" open the resources for the stack and make note of the LambdaFunction value.

Next click on the function button that is located on the environment tab:
![alt text](../resources/image.png)
Provide the accountId and the LambdaFunction value for the function name. Alias can be kept as is and will default to the latest release. 
Click the checkbox for the release you want to deploy and click deploy to the environment that you created the cloudformation stack.

To test that the function is working login to the aws console via the bbc login button on the cosmos accounts page. Find and navigate to your lambda on the lambda page and create a test event to trigger the lambda. You should be able to see the hello world log statement in the function output.