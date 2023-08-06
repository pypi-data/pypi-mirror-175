# properly-util-python

> **Note: This repository is considered legacy, please avoid adding new code to it.**

## Quick Run

1. Setup the environment for development by calling `poetry install`
2. Make your changes to the code
3. Increase the `major` or `minor` values in if appropriate [setup.py](https://github.com/GoProperly/properly-util-python/blob/master/setup.py#L8)
4. Run `./test.sh` to run automated tests.



## Uploading the Package

To upload package.

You can either: 
Merge changes to master branch and push.

*NOTE: You do not need to upload the package, it is uploaded automatically on a merge of a branch to master.* 


## Installing the Package 

`poetry add properly-util-python`

or if your repository has not been updated to use poetry yet:

`pip install properly-util-python`

or

`pip install --no-cache-dir --upgrade properly-util-python`