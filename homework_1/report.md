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
netstat -ep -t 20 -c | grep "homework_1"
```

1. Run command in one terminal window during the programs execution
2. Run program in other terminal window

#### Output

```bash
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 shandra-vb:44772        lb-140-82-121-10-:https ESTABLISHED shandra    94144      6174/./homework_1   
tcp        0      0 localhost:37355         localhost:44478         ESTABLISHED shandra    94128      6174/./homework_1   
tcp        0      0 localhost:44478         localhost:37355         ESTABLISHED shandra    94127      6174/./homework_1   
tcp        0      0 shandra-vb:41568        lb-140-82-121-3-f:https ESTABLISHED shandra    94137      6174/./homework_1   
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 shandra-vb:44772        lb-140-82-121-10-:https ESTABLISHED shandra    94144      6174/./homework_1   
tcp        0      0 localhost:37355         localhost:44478         ESTABLISHED shandra    94128      6174/./homework_1   
tcp        0      0 localhost:44478         localhost:37355         ESTABLISHED shandra    94127      6174/./homework_1   
tcp        0      0 shandra-vb:41568        lb-140-82-121-3-f:https ESTABLISHED shandra    94137      6174/./homework_1   
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 shandra-vb:44772        lb-140-82-121-10-:https ESTABLISHED shandra    94144      6174/./homework_1   
tcp        0      0 localhost:37355         localhost:44478         ESTABLISHED shandra    94128      6174/./homework_1   
tcp        0      0 localhost:44478         localhost:37355         ESTABLISHED shandra    94127      6174/./homework_1   
tcp        0      0 shandra-vb:41568        lb-140-82-121-3-f:https ESTABLISHED shandra    94137      6174/./homework_1   
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 shandra-vb:44772        lb-140-82-121-10-:https ESTABLISHED shandra    94144      6174/./homework_1   
tcp        0      0 localhost:37355         localhost:44478         ESTABLISHED shandra    94128      6174/./homework_1   
tcp        0      0 localhost:44478         localhost:37355         ESTABLISHED shandra    94127      6174/./homework_1   
tcp        0      0 shandra-vb:41568        lb-140-82-121-3-f:https ESTABLISHED shandra    94137      6174/./homework_1   
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 shandra-vb:44772        lb-140-82-121-10-:https ESTABLISHED shandra    94144      6174/./homework_1   
tcp        0      0 localhost:37355         localhost:44478         ESTABLISHED shandra    94128      6174/./homework_1   
tcp        0      0 localhost:44478         localhost:37355         ESTABLISHED shandra    94127      6174/./homework_1   
tcp        0      0 shandra-vb:41568        lb-140-82-121-3-f:https ESTABLISHED shandra    94137      6174/./homework_1
```

Here we can see the connection from the binary(`homework_1`).

#### TODO

- [ ]  Find parameters to run `netstat` such that it is possible to track the number of received/sent bytes by binary

### iostat

Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions.

#### Command line

```bash
iostat -dhkzy 2
```

Explanation: shows device statistisc in human-readable format, in kilobytes per second, display only active devices, skip the first run, update every 2 seconds.

#### Output

```bash
Linux 5.13.0-40-generic (shandra-vb)  01.05.2022  _x86_64_ (1 CPU)


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,50         2,0k        18,0k         0,0k       4,0k      36,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,50         8,0k         0,0k         0,0k      16,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,50        38,0k         0,0k         0,0k      76,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
    41,00         1,7M         6,0k         0,0k       3,4M      12,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,99        10,0k        17,9k         0,0k      20,0k      36,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     0,50         2,0k         0,0k         0,0k       4,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     0,50         2,0k         0,0k         0,0k       4,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     2,00         4,0k        14,0k         0,0k       8,0k      28,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     4,98        17,9k        19,9k         0,0k      36,0k      40,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,50        20,0k         0,0k         0,0k      40,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     0,50         4,0k         0,0k         0,0k       8,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,00         0,0k        16,0k         0,0k       0,0k      32,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
    10,00       266,0k         0,0k         0,0k     532,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
   105,94         1,3M        11,8M         0,0k       2,7M      23,8M       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
    42,00       140,0k        12,0M         0,0k     280,0k      24,1M       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
   190,50         2,0M        13,7M         0,0k       3,9M      27,5M       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
    23,50       132,0k         1,3M         0,0k     264,0k       2,6M       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     1,00         0,0k        23,9k         0,0k       0,0k      48,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     8,50       116,0k        24,0k         0,0k     232,0k      48,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     4,50        34,0k         0,0k         0,0k      68,0k       0,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
    37,00       236,0k        10,0k         0,0k     472,0k      20,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
     0,50         0,0k         4,0k         0,0k       0,0k       8,0k       0,0k sda


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device


      tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device

```

From this output that parameter `kB_wrtn/s` (kilobytes written in second) `kB_read/s`, `kB_read`, `kB_wrtn` were increased during the program run. The usual values were in K. During the program run, the values have increase to the order of M.

```bash
    tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
  105,94         1,3M        11,8M         0,0k       2,7M      23,8M       0,0k sda

    tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
  42,00       140,0k        12,0M         0,0k     280,0k      24,1M       0,0k sda

    tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
  190,50         2,0M        13,7M         0,0k       3,9M      27,5M       0,0k sda

    tps    kB_read/s    kB_wrtn/s    kB_dscd/s    kB_read    kB_wrtn    kB_dscd Device
  23,50       132,0k         1,3M         0,0k     264,0k       2,6M       0,0k sda
  ```

### perf

Performance analysis tools for Linux.

#### Run tool

```bash
sudo perf record --sample-cpu -d fp ./homework_1 
```

#### Report ananlysis

Command generates `perf.data` file. To get an information out of it run

```bash
sudo perf report
```

The top output

```bash
Samples: 6K of event 'cpu-clock:pppH', Event count (approx.): 1581000000
Overhead  Command     Shared Object            Symbol
  34,74%  homework_1  [vboxguest]              [k] vbg_req_perform                                                                           ◆
  28,08%  homework_1  homework_1               [.] fib                                                                                       ▒
  11,81%  homework_1  [e1000]                  [k] e1000_xmit_frame                                                                          ▒
   3,91%  homework_1  [e1000]                  [k] e1000_clean                                                                               ▒
   1,20%  homework_1  [e1000]                  [k] e1000_alloc_rx_buffers                                                                    ▒
   0,66%  homework_1  [kernel.kallsyms]        [k] crc32c_intel_update                                                                       ▒
   0,63%  homework_1  [kernel.kallsyms]        [k] __kmalloc                                                                                 ▒
   0,63%  homework_1  [kernel.kallsyms]        [k] memset                  
```

#### Summary report

```bash
perf report --stdio --show-nr-samples --percent-limit=1
```

```bash
# Total Lost Samples: 0
#
# Samples: 9K of event 'cpu-clock:pppH'
# Event count (approx.): 2397250000
#
# Overhead       Samples  Command     Shared Object            Symbol                                >
# ........  ............  ..........  .......................  ......................................>
#
    54.93%          5267  homework_1  [vboxguest]              [k] vbg_req_perform
    23.44%          2248  homework_1  homework_1               [.] fib
     7.47%           716  homework_1  [e1000]                  [k] e1000_xmit_frame
```

Function `fib` (Fibonacci number calculation with recursion) takes a lot of io CPU resources.

#### Call graps generation

```bash
sudo perf record --call-graph fp ./homework_1 
```

Will create a call graph for a program. Here the recursion will be highly visible. The reccomendation I've got is `Check IO/CPU overload!`.

Call graph for recursive function

```bash
56.40%     0.00%             0  homework_1  libc-2.31.so             [.] __libc_start_main
            |
            ---__libc_start_main
               main
               |          
               |--54.44%--i_like_to_repeat_myself
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          fib
               |          |          
               |           --54.40%--fib
               |                     |          
               |                      --54.37%--fib
               |                                fib
               |                                |          
               |                                 --54.31%--fib
```

### gprof

Before profiling the program shall be build with `-pg` flag.

```bash
cmake -DCMAKE_CXX_FLAGS=-pg -DCMAKE_EXE_LINKER_FLAGS=-pg -DCMAKE_SHARED_LINKER_FLAGS=-pg ../
cmake --build .
```

Then run a program and run `gprog`.

```bash
./homework_1
gprof2dot homework_1 | dot -Tsvg -o output.svg
```

TODO: Fix execution error for now.

## Summary

- `strace` - non-optimal writing to file patterns in avid_writer
- `netstat` - shows high network usage in `homework_1` binary but does not give information about specific function
- `iostat` - disk activity in total but does not give information about specific functions
- `perf` - a lot of tools for performance profiling. Indicated the most time consuming function `fib` and deep recursion problem. Call graph available.

## Analysis steps

Assume that performance measurement target is execution time and goal is to reduce execution time.

1. Run a general performance profiler which will show the biggest execution time.

### Deep recursion

2. Deep recursion can be easily seen on `perf` logs.

### Sleeping function

2. Commnet out all functions but one.
3. Assumption: look for specific system call for sleep with strace(I have not found one).
4. Repeat 2 and 3 for other function.

### Write to file

2. Commnet out all functions but one.
3. Use `iostat` to understand if the function under analysis has disk activity
4. Repeat 2 and 3 for other function.

### Internet download

2. Commnet out all functions but one.
3. Use `netstat` to understand if the function under analysis has internat activity
4. Repeat 2 and 3 for other function.

## References

- [Linux man pages](https://man7.org/linux/man-page)
- [gprof2dot](https://github.com/jrfonseca/gprof2dot)
