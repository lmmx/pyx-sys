- Process group IDs can be used to associate processes and send `SIGSTOP` to freeze processes at once
- It would be desirable to use these on a per-workspace basis to group the location in a concrete way

To get process metadata as tab-delimited values, use AIX format descriptors and print them as

```sh
ps -Ao "%foo\t%bar\t%baz"
```

**Note:** May need to do some silly dance to avoid `ps` truncating `%a`
[according to this](https://stackoverflow.com/questions/10755036/why-is-the-ps-format-option-a-truncated)

Per `man ps`:

```STDOUT
AIX FORMAT DESCRIPTORS
       This ps supports AIX format descriptors, which work somewhat like the formatting codes of
       printf(1) and printf(3).  For example, the normal default output can be produced with
       this: ps -eo "%p %y %x %c".  The NORMAL codes are described in the next section.

       CODE   NORMAL   HEADER
       %C     pcpu     %CPU
       %G     group    GROUP
       %P     ppid     PPID
       %U     user     USER
       %a     args     COMMAND
       %c     comm     COMMAND
       %g     rgroup   RGROUP
       %n     nice     NI
       %p     pid      PID
       %r     pgid     PGID
       %t     etime    ELAPSED
       %u     ruser    RUSER
       %x     time     TIME
       %y     tty      TTY
       %z     vsz      VSZ
```

My current favourite command ([see](https://twitter.com/permutans/status/1306918247648899095)) is:

```sh
ps jf -A
```

> (piped to `less -R`, which is aliased as `s` in my bashrc)

This gives a 'jobs' view and interprets the process hierarchy as a 'forest' (i.e. like `pstree`),
e.g.

```STDOUT
 PPID   PID  PGID   SID TTY      TPGID STAT   UID   TIME COMMAND
    0     2     0     0 ?           -1 S        0   0:00 [kthreadd]
    2     4     0     0 ?           -1 I<       0   0:00  \_ [kworker/0:0H]
    2     6     0     0 ?           -1 I<       0   0:00  \_ [mm_percpu_wq]
    2     7     0     0 ?           -1 S        0   0:16  \_ [ksoftirqd/0]
    2     8     0     0 ?           -1 I        0   7:43  \_ [rcu_sched]
    2     9     0     0 ?           -1 I        0   0:00  \_ [rcu_bh]
    2    10     0     0 ?           -1 S        0   0:06  \_ [migration/0]
    2    11     0     0 ?           -1 S        0   0:02  \_ [watchdog/0]
    2    12     0     0 ?           -1 S        0   0:00  \_ [cpuhp/0]
    2    13     0     0 ?           -1 S        0   0:00  \_ [cpuhp/1]
...
    0     1     1     1 ?           -1 Ss       0   0:36 /lib/systemd/systemd --system --deserialize
19
    1   827   827   827 ?           -1 Ss     103   2:55 /usr/bin/dbus-daemon --system
--address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
    1   828   828   828 ?           -1 Ss       0   0:02 /usr/sbin/cron -f
    1   830   830   830 ?           -1 Ss       0   1:03 /lib/systemd/systemd-logind
    1   837   837   837 ?           -1 Ssl      0  12:05 /usr/sbin/NetworkManager --no-daemon
...
    1  6719  6719  6719 ?           -1 Ssl      0   3:03 /usr/bin/containerd
 6719 28374 28374  6719 ?           -1 Sl       0   0:07  \_ containerd-shim -namespace moby -workdir /var/lib/containerd/io.containerd.runtime.v1.linux/moby/69ed5b5701ceaf8b95...
28374 28401 28401 28401 pts/0    28401 Ss+     33   0:00      \_ /bin/sh -c jupyter notebook --no-browser --ip=0.0.0.0 --port=9001
28401 28449 28401 28401 pts/0    28401 Sl+     33   1:01      |   \_ /usr/local/bin/python /usr/local/bin/jupyter-notebook --no-browser --ip=0.0.0.0 --port=9001
28449 28488 28488 28488 ?           -1 Ssl     33   0:15      |       \_ /usr/local/bin/python -m ipykernel_launcher -f /var/www/.local/share/jupyter/runtime/kernel-b4888f5c-d9...
28449 31932 31932 31932 ?           -1 Ssl     33   4:26      |       \_ /usr/local/bin/python -m ipykernel_launcher -f /var/www/.local/share/jupyter/runtime/kernel-5f4ff23f-ec...
28449  3897  3897  3897 ?           -1 Ssl     33   0:15      |       \_ /usr/local/bin/python -m ipykernel_launcher -f /var/www/.local/share/jupyter/runtime/kernel-c09463af-86...
28449  9183  9183  9183 ?           -1 Ssl     33   0:17      |       \_ /usr/local/bin/python -m ipykernel_launcher -f /var/www/.local/share/jupyter/runtime/kernel-adfb5a5b-34...
28374  8518  8518  8518 pts/1     8524 Ss      33   0:00      \_ bash
 8518  8524  8524  8518 pts/1     8524 S+      33   0:00          \_ scip
    1  6905  6905  6905 ?           -1 Ssl      0   3:12 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
 6905 28366  6905  6905 ?           -1 Sl       0   0:02  \_ /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 9001 -container-ip 172.17.0.2 -container-port 9001

```

I may want others, but to replicate the useful output from `ps jf -A` we can use:

- `%P` for PPID
- `%p` for PID
- `%r` for PGID
- `?` for SID
  - unclear that this would be needed since PGID is available
- `y` for TTY
- `?` for TPGID
  - this is "ID of the foreground process group on the tty (terminal) that the process is connected to,
    or -1 if the process is not connected to a tty."
  - it is -1 for all processes except those whose TTY is a PTS (pseudoterminal slave)
  - I suspect this can be found via window manager anyway?
- `?` for STAT
  - refers to [`stat`](https://en.wikipedia.org/wiki/Stat_(system_call)) system calls
  - see [this Q&A](https://askubuntu.com/questions/360252/what-do-the-stat-column-values-in-ps-mean)
  - `S` means "interruptible sleep", `s` means "is a session leader", `+` means "is in the foreground process group",
    `l` means "is multi-threaded", `<` means "high priority (not nice to other users)", "N" means nice, `Z` means zombie
    process (terminated but not reaped by its parent process), `L` means "has pages locked into memory"
- `?` for UID
- `%x` for TIME
  - cumulative CPU time (distinct from elapsed time `ETIME`
- `%a` and `%c` for COMMAND
  - command with all its arguments as a string (N.B. truncated sometimes) vs. command executable name only

