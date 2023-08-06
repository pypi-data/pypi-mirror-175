# properly-util-python

> **Note: This repository is considered legacy, please avoid adding new code to it.**

## Quick Run

1. Setup the environment for development by calling `poetry install`
2. Activate the virtual environment using `poetry shell`
3. Make your changes to the code
4. Increase the `major` or `minor` values in [setup.py](https://github.com/GoProperly/properly-util-python/blob/master/setup.py#L8) if appropriate 
5. Run `inv test` to run automated tests.



## Uploading the Package

*You do not need to upload the package, it is uploaded automatically on a merge of a branch to main.*


## Installing the Package 

`poetry add properly-util-python`

or if your repository has not been updated to use poetry yet:

`pip install properly-util-python`

or

`pip install --no-cache-dir --upgrade properly-util-python`