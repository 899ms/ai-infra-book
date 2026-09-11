"""Derived teaching examples; saved measurements remain untouched."""
import json
import math
from fractions import Fraction

def compute(root):
    def source(name):
        return json.loads((root / ('calculations/results/'+name+'.json')).read_text())['summary']
    MiB=2**20
    # Per-round startup: public nccl-tests on two HGX H100 + ConnectX-7 servers (experiments/ch07/07-03),
    # 16-rank AllReduce of 16-128 B takes about 25 us; spread over the 30 rounds of a 16-rank ring.
    alpha=833e-9
    # Book configuration: two HGX-class servers, eight ranks each, one 50 GB/s NIC per rank,
    # NVLink 450 GB/s per direction. Sixteen ranks, 12 MiB ring chunks.
    local=450e9
    nic=50e9
    ranks=8
    p=2*ranks
    chunk=12*MiB
    def flat(bl=local,bn=nic):
        return 2*(p-1)*(alpha+max(chunk/bl,chunk/bn))
    def hier(bl=local,bn=nic,nics=ranks):
        return 2*(ranks-1)*(alpha+2*chunk/bl)+2*(alpha+(ranks/nics)*chunk/bn)
    saved={name:float(Fraction(source(name)['serial_barrier_lower_seconds_exact'])) for name in ['gradient-fp32-flat-contiguous-nic8','gradient-fp32-flat-interleaved-nic8','gradient-fp32-hierarchical-nic8','gradient-fp32-hierarchical-nic1']}
    # Contrast configuration: four A100 80GB PCIe per server, GPU peer-to-peer over PCIe Gen4 x16 (32 GB/s),
    # one dual-port ConnectX-7 (2 x 200 GbE = 2 x 25 GB/s) in a PCIe Gen4 x16 slot (32 GB/s per direction).
    c_local=32e9
    c_exit=32e9
    c_bridge=300e9  # A100 PCIe NVLink bridge, 600 GB/s bidirectional
    def flat_c(bl=c_local,br=c_exit,nics=2):
        return 14*(alpha+max(24*MiB/bl,24*MiB/min(br,nics*25e9)))
    def hier_c(bl=c_local,br=c_exit):
        return 6*(alpha+48*MiB/bl)+2*(alpha+96*MiB/br)
    saved_c={name:float(Fraction(source(name)['serial_barrier_lower_seconds_exact'])) for name in ['gradient-fp32-flat-contiguous-two-nic','gradient-fp32-flat-interleaved-two-nic','gradient-fp32-hierarchical-two-nic','gradient-fp32-flat-contiguous-one-nic','gradient-fp32-flat-contiguous-three-nic']}
    state=source('remote-state-reused')
    read_s=float(Fraction(state['remote_per_read_exact_ns']))/1e9
    local_s=float(Fraction(state['local_per_read_exact_ns']))/1e9
    setup_s=float(Fraction(state['stage_setup_exact_ns']))/1e9
    window_Bps=128*256/2e-6
    # Issue interval: RoCE reliable connection in the OpenURMA toolchain, 6 cycles at 322 MHz (ub-fabric-book).
    fabric=json.loads((root/'calculations/results/ub-fabric-book.json').read_text())
    delta=fabric['throughput']['roce_interval_ns']*1e-9
    pcie_read_s=fabric['summary']['roce_dma_round_trip_ns']*1e-9
    a=hier();b=flat();w=hier(bn=window_Bps);one=hier(nics=1)
    step=lambda ready,t:max(.020,ready+t)+.002
    return {
        'kind':'derived teaching models, not measurements',
        'primary':{'participants':p,'ranks_per_server':ranks,'per_rank_bytes':192*MiB,'chunk_bytes':chunk,'nics_per_server':ranks,'nic_Bps':nic,'local_Bps':local,'round_startup_s':alpha,'flat_s':b,'interleaved_s':flat(),'hier_s':a,'hier_one_nic_s':one,'saved_s':saved,'local_crossover_Bps':2*(ranks-1)*2*chunk/(b-2*(alpha+chunk/nic)-2*(ranks-1)*alpha)},
        'contrast':{'participants':8,'ranks_per_server':4,'per_rank_bytes':192*MiB,'nics_per_server':2,'nic_Bps':25e9,'shared_per_direction_Bps':c_exit,'local_bridge_Bps':c_bridge,'local_Bps':c_local,'flat_s':flat_c(),'hier_s':hier_c(),'saved_s':saved_c,'flat_local_bridge_s':flat_c(bl=c_bridge),'hier_local_bridge_s':hier_c(bl=c_bridge),'port_Bps':25e9,'two_ports_unshared_s':14*(alpha+24*MiB/50e9),'expert_ingress_s':32*MiB/c_exit,'local_crossover_Bps':288*MiB/(144*MiB/c_exit+6*alpha),'flat_one_nic_s':flat_c(nics=1),'flat_three_nic_s':flat_c(nics=3)},
        'scaling':{'compute_s':.020,'cut_volume_bytes':360*MiB,'cut_Bps':nic,'cut_s':360*MiB/nic,'crossover_device_multiplier':.020/(360*MiB/nic)},
        'small_messages':{'bandwidth_Bps':50e9,'tripled_Bps':150e9,'startup_s':5e-6,'single_message_crossover_bytes':5e-6*50e9,'ring_crossover_bytes':14*5e-6*50e9/1.75,'ring_8MiB_s':[14*5e-6+1.75*8*MiB/b for b in (50e9,150e9)],'ring_8KiB_s':[14*5e-6+1.75*8192/b for b in (50e9,150e9)],'serial_72_bandwidth_saving_s':72*1.75*8192*(1/50e9-1/150e9),'serial_72_startup_saving_s':72*14*(5e-6-2e-6),'serial_step_1MB_s':[5e-6+1e6/b for b in (50e9,100e9)],'serial_step_10KB_s':[5e-6+1e4/b for b in (50e9,100e9)]},
        'pipeline':{'stages':4,'microbatches':8,'stage_s':.001,'finish_s':.011,'utilization':8/11,'microbatches_for_90pct':27},
        'independent_reads':{'reads':8,'per_read_s':pcie_read_s,'serial_s':8*pcie_read_s,'parallel_s':pcie_read_s},
        'snapshot':{'payload_bytes':144*MiB,'remote_per_read_s':read_s,'local_per_read_s':local_s,'setup_s':setup_s,'full_reuse_boundary':setup_s/(read_s-local_s),'full_first_winning_integer':math.floor(setup_s/(read_s-local_s))+1,'ten_pct_reuse_boundary':setup_s/(.1*(read_s-local_s)),'ten_pct_first_winning_integer':math.floor(setup_s/(.1*(read_s-local_s)))+1},
        'window':{'transaction_bytes':256,'lifetime_s':2e-6,'path_Bps':nic,'active_128_Bps':window_Bps,'required_active_256':math.ceil(nic*2e-6/256),'required_active_4096':math.ceil(nic*2e-6/4096),'required_start_interval_s':256/nic,'issue_interval_s':delta,'issue_rate_per_s':1/delta,'rate_256_at_delta_Bps':256/delta,'rate_4096_at_delta_Bps':4096/delta,'start_interval_4096_s':4096/nic,'rate_bound_crossover_bytes':delta*nic},
        'isolation':{'fixed_bytes':64*256+64*128*64,'per_class_bytes':128*1024,'budget_bytes':MiB,'max_classes':(MiB-64*256-64*128*64)//(128*1024)},
        'reclaim':{'operation_bytes':8192,'consumed_per_poll':4,'poll_s':20e-6,'sustainable_Bps':4*8192/20e-6,'required_rate_ops_per_s':nic/8192,'required_interval_s':8192/nic},
        'queue':{'buffer_bytes':512*1024,'excess_Bps':50e9,'max_overlap_s':512*1024/50e9,'feedback_max_s':256*1024/50e9},
        'multipath':{'packet_bytes':4096,'rate_Bps':nic,'packet_serialization_s':4096/nic,'single_s':8*4096/nic+1e-6,'balanced_s':4*4096/nic+1e-6,'delay_difference_boundary_s':4*4096/nic},
        'step':{'compute_s':.020,'update_s':.002,'flat_serial_s':.020+b+.002,'hier_serial_s':.020+a+.002,'hier_window_limited_comm_s':w,'hier_window_limited_serial_s':.020+w+.002,'flat_ready_17ms_s':step(.017,b),'hier_ready_17ms_s':step(.017,a),'hier_last_ready_fully_hidden_s':.020-a,'hier_one_nic_comm_s':one,'hier_one_nic_ready_17ms_s':step(.017,one)}
    }
