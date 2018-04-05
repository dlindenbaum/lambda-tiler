# lambda-tiler

#### AWS Lambda + rio-tiler to serve tiles from any web hosted files

An online service is available for anyone to use with Cloud Optimized GeoTIFF's

Sample Bounds Request:

https://bstlgagxwg.execute-api.us-east-1.amazonaws.com/production/bounds?url=http://oin-hotosm.s3.amazonaws.com/593ee29de407d7001138613d/0/d42dec6e-3682-4d49-8d01-5755483671eb.tif

Sample Tile Request:

https://bstlgagxwg.execute-api.us-east-1.amazonaws.com/production/tiles/21/1087689/1046434.png?url=http://oin-hotosm.s3.amazonaws.com/593ee29de407d7001138613d/0/d42dec6e-3682-4d49-8d01-5755483671eb.tif

# Info


---

# Installation

##### Requirement
  - AWS Account
  - Docker
  - node + npm


#### Create the package

```bash
# Build Amazon linux AMI docker container + Install Python modules + create package
git clone https://github.com/vincentsarago/lambda-tiler.git
cd lambda-tiler/
make all
```

#### Deploy to AWS

```bash
#configure serverless (https://serverless.com/framework/docs/providers/aws/guide/credentials/)
npm install
sls deploy
```

# Endpoint

## /bounds

*Inputs:*
- url: any valid url

*example:*
```
$ curl {you-endpoint}/bounds?url=https://any-file.on/the-internet.tif

  {"url": "https://any-file.on/the-internet.tif", "bounds": [90.47546096087822, 23.803014490532913, 90.48441996322644, 23.80577697976369]}
```

#### /tiles/z/x/y.png

*Inputs:*
- url: any valid url

*Options:*
- rgb: select bands indexes to return (e.g: (1,2,3), (4,1,2))
- nodata: nodata value to create mask

*example:*
```
$ curl {you-endpoint}/tiles/7/10/10.png?url=https://any-file.on/the-internet.tif

```
