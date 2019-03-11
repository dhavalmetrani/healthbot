"""
This is the main entrypoint of code.
"""
import sys
import lib.summary as summary
import lib.aws_comprehend as aws_comprehend
import requests

IDENTITY={}
try:
  IDENTITY = json.loads(requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document').json())
except Exception as ex:
  IDENTITY={
    "version" : "2017-09-30",
    "devpayProductCodes" : None,
    "marketplaceProductCodes" : None,
    "instanceType" : "t2.micro",
    "pendingTime" : "2019-03-10T03:06:07Z",
    "imageId" : "ami-00158b185c8cc09dc",
    "billingProducts" : None,
    "instanceId" : "i-01d747c16dd879961",
    "accountId" : "500502477419",
    "availabilityZone" : "ap-southeast-1a",
    "kernelId" : None,
    "ramdiskId" : None,
    "architecture" : "x86_64",
    "privateIp" : "172.31.20.210",
    "region" : "ap-southeast-1"
  }
AWS_REGION = IDENTITY['region']
PARA = "```{}```"
BOLD = "*{}*"
ITALIC = "_{}_"


def main():
  """
  Main function.
  """
  # print(len(sys.argv))
  # print(sys.argv[0])
  # if len(sys.argv) <= 1:
    # print("Need a text to process.")

    # sys.exit(0)
  input_string = " ".join(sys.argv[1:])
  LE = aws_comprehend.LanguageEngine(AWS_REGION)

  txt = LE.get_dominant_language(input_string)
  print(BOLD.format("Dominant Language"))
  print(PARA.format(txt))

  txt = LE.get_key_phrases(input_string)
  print(BOLD.format("Key Phrases"))
  print(PARA.format(txt))

  LEM = aws_comprehend.LanguageEngineMedical('us-west-2')
  txt = LEM.get_entities(input_string)
  print(BOLD.format("Entities (Medical)"))
  print(PARA.format(txt))



if __name__ == '__main__':
  """
  Main guard.
  """
  main()
