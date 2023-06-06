# Dockerfile : InTeractively run OJ

FROM nitin12384/django:v1

# Copy problem data
ADD ./data /root/data

# Copy the code and database of OJ
ADD ./oj_django_project /root/oj_django_project

# Since we are using my image nitin12384/django:v1, we already have all requirements installed
# RUN pip install -r /root/oj_django_project/requirements.txt
# G++ and python are also preinstalled

####################################################
# Build with `docker build -t ojit1 -f it.dockerfile .`

# -d for detached ?
####################################################
# Run with `docker run --name ojitcont1 -it -p 8072:8072 -e OS_TYPE=UBUNTU_DOCKERIZED ojit1 /bin/bash`
# Do `python /root/oj_django_project/manage.py runserver 0.0.0.0:8072 --noreload`