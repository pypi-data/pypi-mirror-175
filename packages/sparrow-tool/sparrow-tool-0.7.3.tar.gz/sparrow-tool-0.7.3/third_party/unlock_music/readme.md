# Unlock Music Project
https://github.com/unlock-music/cli

使用方式  

```
.\um-windows-amd64.exe -i <输入文件夹> -o <输出文件夹>   
```

# 在线版本
https://github.com/unlock-music/unlock-music

docker 镜像 (非官方，官方已经下架了)  
```bash
kofua/unlock-music:latest
```
启动
```bash
docker run --name unlock-music -d -p 8080:80 kofua/unlock-music
```
服务 http://localhost:8080
