# lambda-layer-example

This is a sample SAM template for creating a Lambda Layer using Python. For an example of utilizing this layer in a lambda, see [https://github.com/mcbanderson/lambda-utilize-layer-example](https://github.com/mcbanderson/lambda-utilize-layer-example)

The following is an overview of what is provided in this repository.

```bash
.
├── README.md                   <-- This README file
├── .travis.yml                 <-- Example travisci pipeline
├── src                         <-- Source code for our lambda layer
│   ├── __init__.py
│   ├── my_module.py            <-- The module your layer will provide
│   ├── requirements.txt        <-- Module requirements
├── template.yaml               <-- SAM Template
└── tests                       <-- Unit tests
    └── unit
        ├── __init__.py
        └── test_handler.py
```

## Requirements

* AWS CLI already configured
* SAM CLI installed
* [Python 3 installed](https://www.python.org/downloads/)

## Setup

### Creating Your Layer

The first step is to create the module or package you want your Lambda Layer to provide. In this case we have created a module, `my_module.py`, which contains a single function, `my_function()`, which simply returns the value of the numpy constant `numpy.e`.

Once you have created your module/package, we need to specify an AWS SAM LayerVersion in our SAM template (`template.yaml`).

```yaml
Resources:
    MyLayer:
        Type: AWS::Serverless::LayerVersion
        Properties:
            CompatibleRuntimes:
                - python3.6
                - python3.7
            ContentUri: dist/
            Description: A sample lambda layer
            LayerName: my_layer
```

Notice that we have specified `ContentUri: dist/`. For this example we will copy our module to `dist/` before we package it, but you can use whatever directory name you like, as it has no effect once the Layer has been packaged.

### Packaging and Deploying

Before we can package and deploy our Layer, we need an `S3 bucket` where we can upload our packaged Lambda Layer - If you don't have an S3 bucket to store code artifacts in, then this is a good time to create one:

```bash
aws s3 mb s3://<BUCKET_NAME>
```

Next we need to create a directory to put our module in for packaging. The name of this directory doesn't matter, but for this example we'll name it `dist`.

```bash
mkdir dist
```

We also need to create a directory within `dist/`, named `python`, in which we will place our module and its dependencies. THE NAME OF THIS DIRECTORY MUST BE `python`, otherwise our module will not be accessible to our Lambda. See the [Lambda Layer docs](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-path) for more info.

```bash
mkdir dist/python
```

Now we will copy our module to `dist/python/`, as well as any `pip` packages required by our module.

```bash
cp src/my_module.py dist/python
pip install -r src/requirements.txt -t dist/python
```

Now we are finally ready to package and deploy our Layer. To package, run:

```bash
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket <BUCKET_NAME>
```

And to deploy it, run:

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name <STACK_NAME> \
```

And that's it! Once your Stack is deployed, your Layer will be ready to use.

## Using Your Layer

You may have noticed that we provided an `SSM Parameter` in our `template.yaml`. This is included so we can easily include our Layer in our Lambdas. As mentioned earlier, you can go to [https://github.com/mcbanderson/lambda-utilize-layer-example](https://github.com/mcbanderson/lambda-utilize-layer-example) to see an example of how to utilize your new Layer.

## Cleanup

In order to delete our Layer, we just need to delete the CloudFormation stack that was created. To do so use the following AWS CLI command:

```bash
aws cloudformation delete-stack --stack-name <STACK_NAME>
```
