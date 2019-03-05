"""
This is the main entrypoint of code.
"""
import sys

def main():
  """
  Main function.
  """
  # print(len(sys.argv))
  # print(sys.argv[0])
  if len(sys.argv) <= 1:
    print("Need a text to process.")
    sys.exit(1)
  input_string = " ".join(sys.argv[1:])
  print("Input string: " + input_string)


if __name__ == '__main__':
  """
  Main guard.
  """
  main()
