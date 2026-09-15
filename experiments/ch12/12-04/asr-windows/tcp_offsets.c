#include <stdio.h>
#include <stddef.h>
#include <linux/tcp.h>
#define FIELD(name) printf("\"" #name "\":%zu,", offsetof(struct tcp_info,name));
int main(void) { printf("{"); FIELD(tcpi_snd_wnd); FIELD(tcpi_rcv_space); FIELD(tcpi_snd_cwnd); FIELD(tcpi_snd_mss); FIELD(tcpi_rtt); FIELD(tcpi_rwnd_limited); FIELD(tcpi_sndbuf_limited); FIELD(tcpi_busy_time); FIELD(tcpi_total_retrans); printf("\"sizeof\":%zu}\n",sizeof(struct tcp_info)); }
