import requests
import sys
import json
import argparse


if __name__ == '__main__':

  argp = argparse.ArgumentParser()
  argp.add_argument('-u', '--url', required=True, help="Base url for the RAG server. ")
  argp.add_argument('-i', '--index', help="Indexes a file")
  argp.add_argument('-q', '--query', help="Make a question")
  argp.add_argument('-e', '--embeddings', help="Generate embeddings for text")
  argp.add_argument('-n', '--ner', help="Perform Name Ententiy Recognition actions")
  argp.add_argument('--debug', help="Get debug information from server")
  argp.add_argument('--text_file', default="pdf", help="Sets the upload file of text format. default is PDF")
  
  args = argp.parse_args()


  url = args.url.strip('/')

  data_to_post = dict()
  data_to_post["debug"] = False
  data_to_post["options"] = dict()

  if args.debug:
    data_to_post["debug"] = True

  if args.query:
    data_to_post["query"] = args.query
    r = requests.post(url=f"{url}/api/v1/query", json=data_to_post, verify=False)
    c = r.content.decode("UTF-8")
    print(c)
    sys.exit()

  if args.embeddings:
    data_to_post["query"] = args.embeddings
    r = requests.post(url=f"{url}/api/v1/embed", json=data_to_post, verify=False)
    c = r.content.decode("UTF-8")
    print(c)
    sys.exit()
  
  if args.ner:
    data_to_post["query"] = args.ner
    r = requests.post(url=f"{url}/api/v1/ner", json=data_to_post, verify=False)
    c = r.content.decode("UTF-8")
    print(c)
    sys.exit()

  if args.index:
    options = {'type':'file', "file_type": args.text_file}
  
    try:
      fp = {'file': open(args.index,'rb')}
    except Exception as e:
      print(f"unable to read file {args.index}")
      sys.exit(-1)

    r = requests.post(url=url + '/api/v1/upload/file', files=fp, verify=False)
    file_name = r.json()
    file_name = file_name["details"]['filename']
    metadata = {"filename": args.index}
    
    r = requests.post(url=url + '/api/v1/index/document', json={"text":file_name, "options": options, "metadata": metadata})
    print(r.content)
  
  