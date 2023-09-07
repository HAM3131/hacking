#!/usr/bin/env bash
mkdir -p /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
chown nimr /sys/fs/cgroup/{cpu,memory,pids}/NSJAIL
su - nimr -c "nsjail --config /opt/app/jail.cfg -- $@"
rm $@
