from ollama_client import ping

if __name__=='__main__':
  ok=ping()
  print('ollama_ok=' + str(ok).lower())
