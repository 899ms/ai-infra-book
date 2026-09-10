"""Derived teaching examples; saved measurements remain untouched."""
import json
import math
from fractions import Fraction

def compute(root):
    def source(name):
        return json.loads((root / ('calculations/results/'+name+'.json')).read_text())['summary']
    MiB=2**20
    alpha=2e-6
    local=200e9
    remote=40e9
    def flat(bl=local,br=remote,nics=2):
        return 14*(alpha+max(24*MiB/bl,24*MiB/min(br,nics*25e9)))
    def hier(bl=local,br=remote):
        return 6*(alpha+48*MiB/bl)+2*(alpha+96*MiB/br)
    saved={name:float(Fraction(source(name)['serial_barrier_lower_seconds_exact'])) for name in ['gradient-fp32-flat-contiguous-nic2','gradient-fp32-hierarchical-nic2']}
    state=source('remote-state-reused')
    read_s=float(Fraction(state['remote_per_read_exact_ns']))/1e9
    local_s=float(Fraction(state['local_per_read_exact_ns']))/1e9
    setup_s=float(Fraction(state['stage_setup_exact_ns']))/1e9
    window_Bps=128*256/2e-6
    a=hier();b=flat();w=hier(br=window_Bps);slow=hier(br=20e9)
    step=lambda ready,t:max(.020,ready+t)+.002
    return {
        'kind':'derived teaching models, not measurements',
        'primary':{'participants':8,'per_rank_bytes':192*MiB,'nics_per_server':2,'nic_Bps':25e9,'shared_per_direction_Bps':remote,'local_Bps':local,'round_startup_s':alpha,'flat_s':b,'hier_s':a,'saved_s':saved,'flat_local_50GBs_s':flat(bl=50e9),'hier_local_50GBs_s':hier(bl=50e9),'local_crossover_Bps':288*MiB/(144*MiB/remote+6*alpha),'flat_one_nic_s':flat(nics=1)},
        'scaling':{'compute_s':.020,'cut_volume_bytes':336*MiB,'cut_s':336*MiB/remote,'crossover_device_multiplier':.020/(336*MiB/remote)},
        'small_messages':{'bandwidth_Bps':25e9,'startup_s':5e-6,'single_message_crossover_bytes':5e-6*25e9,'ring_crossover_bytes':14*5e-6*25e9/1.75,'serial_72_bandwidth_saving_s':72*1.75*8192*(1/25e9-1/75e9),'serial_72_startup_saving_s':72*14*(5e-6-2e-6)},
        'pipeline':{'stages':4,'microbatches':8,'stage_s':.001,'finish_s':.011,'utilization':8/11,'microbatches_for_90pct':27},
        'snapshot':{'payload_bytes':144*MiB,'remote_per_read_s':read_s,'local_per_read_s':local_s,'setup_s':setup_s,'full_reuse_boundary':setup_s/(read_s-local_s),'full_first_winning_integer':math.floor(setup_s/(read_s-local_s))+1,'ten_pct_reuse_boundary':setup_s/(.1*(read_s-local_s)),'ten_pct_first_winning_integer':math.floor(setup_s/(.1*(read_s-local_s)))+1},
        'window':{'transaction_bytes':256,'lifetime_s':2e-6,'active_128_Bps':window_Bps,'required_active_256':math.ceil(remote*2e-6/256),'required_active_4096':math.ceil(remote*2e-6/4096),'required_start_interval_s':256/remote,'rate_4096_at_100ns_Bps':4096/1e-7},
        'isolation':{'fixed_bytes':64*256+64*128*64,'per_class_bytes':128*1024,'budget_bytes':MiB,'max_classes':(MiB-64*256-64*128*64)//(128*1024)},
        'reclaim':{'operation_bytes':8192,'consumed_per_poll':4,'poll_s':20e-6,'sustainable_Bps':4*8192/20e-6,'required_rate_ops_per_s':remote/8192,'required_interval_s':8192/remote},
        'queue':{'buffer_bytes':512*1024,'excess_Bps':30e9,'max_overlap_s':512*1024/30e9,'feedback_max_s':256*1024/30e9},
        'multipath':{'packet_bytes':1024,'rate_Bps':1e9,'single_s':8*1024/1e9+1e-6,'balanced_s':4*1024/1e9+1e-6,'delay_difference_boundary_s':4*1024/1e9},
        'step':{'compute_s':.020,'update_s':.002,'flat_serial_s':.020+b+.002,'hier_serial_s':.020+a+.002,'hier_window_limited_comm_s':w,'hier_window_limited_serial_s':.020+w+.002,'flat_ready_17ms_s':step(.017,b),'hier_ready_17ms_s':step(.017,a),'hier_ready_12ms_s':step(.012,a),'hier_last_ready_fully_hidden_s':.020-a,'hier_slow_comm_s':slow,'hier_slow_ready_17ms_s':step(.017,slow)}
    }
