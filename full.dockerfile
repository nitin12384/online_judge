# Dockerfile

FROM nitin12384/django:v1

# Copy problem data
ADD ./data /root/data

# Copy the code and database of OJ
ADD ./oj_django_project /root/oj_django_project

# Since we are using my image nitin12384/django:v1, we already have all requirements installed
# RUN pip install -r /root/oj_django_project/requirements.txt
# G++ and python are also preinstalled

# To configure the environment
ARG OS_TYPE=UBUNTU_DOCKERIZED

# used --noreload, because otherwise it gets stuck at "Watching for file changes with statsreloader"
# There may be one more way to do so, by Setting ENV variable PYTHONBUFFERED to 1, 
# but I dont know how to do that for now
# port as "8071" or "127.0.0.1:8071" wont work. 
CMD ["python", "/root/oj_django_project/manage.py", "runserver", "0.0.0.0:8071", "--noreload"]

# Build with `docker build -t oj1 -f full.dockerfile .`

# -d for detached ?
# Run with `docker run --name ojcont2 -d -p 8072:8072 oj1`