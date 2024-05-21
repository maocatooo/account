docker build -t acc_backend .

docker run --name acc_backend -env-file=.env -p 8888:8888 -d acc_backend