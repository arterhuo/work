# work
  - 添加安全码用于自动计算 tfa
    - java -jar gauth.jar TWSJG2D4MC4LSDfA name
  - 之后使用 java -jar gauth.jar 既可获得tfa numbers

  - .ssh/config 
  ```Host *
    SendEnv LANG LC_*
    ControlMaster auto
    ControlPath /tmp/ssh_mux_%h_%p_%r
    ControlPersist 100h
  ```
