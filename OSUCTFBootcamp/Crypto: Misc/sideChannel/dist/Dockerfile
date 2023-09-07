FROM nsjailcontainer

RUN apt-get update && \
apt-get install -y \
    lib32z1 \
    gcc-multilib \
    uidmap \
    python3 \
    python3-pip \
    locales && \
rm -rf /var/lib/apt/lists/* && \
locale-gen en_US && locale-gen en_US.UTF-8 && \
pip3 install fastapi uvicorn aiofiles

ADD server.py run_jail.sh flag.txt /opt/app/
ADD static /opt/app/static
ADD jails /opt/app/jails
ADD jailyard/ /opt/jailyard

# Create jailed user
RUN useradd -m inmate && \
#
# Set up nsjail chroot
mkdir /chroot/ && \
chown inmate:inmate /chroot && \
chmod 770 /chroot && \
#
chmod 440 /opt/app/flag.txt && \
chmod +x /opt/app/run_jail.sh && \
chmod +x /opt/jailyard/compile.sh && \
#
mkdir /opt/transfer && \
chown root:inmate /opt/transfer && \
chmod 770 /opt/transfer

WORKDIR /opt/app

ENV LC_ALL=C.UTF-8 \
LANG=C.UTF-8

CMD python3 -m uvicorn server:app --host 0.0.0.0 --port 8000

# # socat needs -s because otherwise it randomly exits due to `timeout`
# CMD socat -d -d -s TCP-LISTEN:9000,reuseaddr,fork,max-children=8 EXEC:'timeout 4m /usr/bin/python3 -u /opt/app/server.py'
