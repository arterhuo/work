# work
  - 添加安全码用于自动计算 tfa
    - java -jar gauth.jar TWSJG2D4MC4LSDfA name
  - 之后使用 java -jar gauth.jar 既可获得tfa numbers

  - .ssh/config 
  ```
  Host jump
      HostName bao.hostname
      User username
      Port port
  ```
  - cp jumpserver /usr/local/bin/jump
  ```
    Usage: jump dest_hostname

Options:
  -h, --help  show this help message and exit
  ```
