FROM nsjailcontainer

WORKDIR /opt/app

RUN apt-get update && apt-get install -y \
    lib32z1 \
    gcc-multilib \
    uidmap \
    curl \
    nginx \
&& rm -rf /var/lib/apt/lists/*

ADD sites-available.conf /etc/nginx/sites-available/default
ADD index.html dist.zip /var/www/html/
ADD flag.txt /opt/flag.txt
ADD main.nim jail.cfg run_jail.sh /opt/app/

RUN \
# Create users for executing code submitted through the web server:
# The `nimr` user runs code.
# The `nimc` user compiles code.
useradd -m nimr && \
useradd -m nimc && \
#
# Download and install Nim
cd /tmp && \
curl -O https://nim-lang.org/download/nim-1.4.4-linux_x64.tar.xz && \
tar -xf nim-1.4.4-linux_x64.tar.xz && \
cd nim-1.4.4 && \
./install.sh /usr/bin && \
#
# Give `nimc` user access to Nim
chown root:nimc /usr/bin/nim && \
#
# Set up directory for storing and running compiled programs
# `nimc` can RWX, `nimr` can RX
mkdir /opt/box && \
chown nimc:nimr /opt/box && \
chmod 750 /opt/box && \
#
# Compile the app
cd /opt/app && \
nim c main.nim && \
rm main.nim && \
chown -R root:nimc . && \
chmod -R o-wx * && \
#
# Set up nsjail chroot
mkdir /chroot/ && \
chown nimr:nimr /chroot && \
chmod 750 /chroot && \
#
# Flag permissions :)
chown root:nimc /opt/flag.txt && \
chmod 440 /opt/flag.txt

CMD nginx && /opt/app/main
