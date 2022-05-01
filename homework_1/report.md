# Lab execution report

## Goal

Figure out what is wrong with a program

## Tools used

### ltrace

#### Command line

```bash
ltrace -f -c ./homework_1
```

#### Result

```bash
Main started...
Started i_like_to_repeat_myself...
0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 6765 10946 17711 28657 46368 75025 121393 196418 317811 514229 832040 1346269 2178309 3524578 5702887 9227465 14930352 24157817 39088169 63245986 102334155 165580141 267914296 433494437 701408733 
i_like_to_repeat_myself finished, duration 11908855 microseconds (11.9089 seconds)
Started sleeping_beauty...
sleeping_beauty finished, duration 5000266 microseconds (5.00027 seconds)
Started avid_writer...
avid_writer finished, duration 18946152 microseconds (18.9462 seconds)
Started does_not_download_anything_really...
downloaded_bytes 25720952
does_not_download_anything_really finished, duration 5515513 microseconds (5.51551 seconds)
% time     seconds  usecs/call     calls      function
------ ----------- ----------- --------- --------------------
------ ----------- ----------- --------- --------------------
100.00    0.000000                     0 total
```

Conclusion: ltrace does not show external library calls. (Why really? The external library is used in the binary. Assumption - it is statically linked, need to check cmake library function).

### strace

Trace system calls and signals.

#### Command line

```bash
strace -c ./homework_1
```

Callind the command wihtout arguments gives too much of output.

#### The most time consuming system calls

```bash
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 89,45    2,563838           1   2500023           write
  7,76    0,222476          32      6913      1178 read
  1,60    0,045972           7      6393           poll
  0,40    0,011587          21       549           close
  0,40    0,011585           1      9620           rt_sigaction
  0,08    0,002397         217        11           munmap
  0,06    0,001796           3       559        22 openat
  0,06    0,001787           3       539        14 stat
  0,06    0,001755           1      1192           fcntl
  0,03    0,000929           0      1060           fstat
  0,03    0,000791           0      1045           lseek
  0,03    0,000791         158         5         2 connect
  0,01    0,000240          60         4           getdents64
  0,00    0,000099           1        61           mmap
  ...
------ ----------- ----------- --------- --------- ----------------
100.00    2,866351               2528092      1218 total
```

Absolute leader in terms of time is "write" system call. This indicates non-optimal writing parrent.

### ldd

Prints the shared objects (shared libraries) required by each program or shared object specified on the command line.

#### Command line

```bash
ldd ./homework_1
```

#### Outputs list of libraries the binary is linked with

```bash
linux-vdso.so.1 (0x00007fff02a98000)
libcpr.so.1 => /home/shandra/code/performance-engineering-ucu/homework_1/build/_deps/cpr-build/cpr/libcpr.so.1 (0x00007f9473707000)
libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f94736d3000)
libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f94734f1000)
libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f94734d6000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f94732e4000)
libcurl-d.so => /home/shandra/code/performance-engineering-ucu/homework_1/build/_deps/curl-build/lib/libcurl-d.so (0x00007f9473222000)
/lib64/ld-linux-x86-64.so.2 (0x00007f947378a000)
libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f94730d3000)
libmbedtls.so.12 => /lib/x86_64-linux-gnu/libmbedtls.so.12 (0x00007f94730a4000)
libmbedx509.so.0 => /lib/x86_64-linux-gnu/libmbedx509.so.0 (0x00007f9473083000)
libmbedcrypto.so.3 => /lib/x86_64-linux-gnu/libmbedcrypto.so.3 (0x00007f9473020000)
```

Here we can see

- linux-vdso.so.1 - virtual dymanic shared object, is called by C library.
- libcpr (also libmbedx509, libmbedcrypto, libcurl-d, libm, libpthread) - C++ wrapper around libcurl.
- libstdc++, libc, libgcc_s - standart libraries.

I do not see how this information can help to identify time delays.

### netstat

Network monitoring tool.

#### Command line

```bash
netstat -ep -t 20
```

1. Run program in one window
2. Run `netstat` in other window during the programs execution

#### Output

```bash
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name    
tcp       25      0 shandra-vb:37774        a104-96-139-12.de:https CLOSE_WAIT  shandra    32976      1364/Code --standar 
tcp        0      0 shandra-vb:44760        lb-140-82-121-10-:https ESTABLISHED shandra    41177      2439/./homework_1   
tcp       64      0 shandra-vb:50884        104.21.2.130:https      CLOSE_WAIT  shandra    32995      1364/Code --standar 
tcp        0      0 localhost:57980         localhost:40551         ESTABLISHED shandra    41160      2439/./homework_1   
tcp        0      0 shandra-vb:33096        lb-140-82-121-4-f:https ESTABLISHED shandra    41170      2439/./homework_1   
tcp        0      0 localhost:40551         localhost:57980         ESTABLISHED shandra    41161      2439/./homework_1
```

Here we can see the connection from the binary(`homework_1`).

#### TODO

- [ ]  Find parameters to run `netstat` such that it is possible to stack the number of received/sent bytes by binary

### iostat

Disk monitoring tool.

## Conclusion

- strace - non-optimal writing to file patterns in avid_writer
- netstat - shows high network usage in does_not_download_anything_really

## References

- [Linux man pages](https://man7.org/linux/man-page)