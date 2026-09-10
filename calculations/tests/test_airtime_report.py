"""Independent report accounting, including future/failed/teaching boundaries."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.report import markdown
from infra_calc.transport.airtime_report import ledger
from infra_calc.transport.media_report import markdown as media_markdown


def fixture():
    return dict(inputs=dict(application=dict(scheduling={'send':'fifo','compute':'fifo'},messages=[],compute_tasks=[]),network=dict(until='1',controller={'name':'newreno'})),summary=dict(complete=False,all_messages_delivered=False,pending_packets={'up':0,'down':0},wire_bytes=1228,serialized_wire_bytes_by_horizon=None,wan_serialized_ip_bytes_by_horizon='1228',unique_received_application_bytes=1,delivered_application_bytes=1),businesses=[],transmissions=[],waits=[],message_status={},sender_events={},final_states={},wireless_summary=dict(observed_reserved_seconds='151/500000'),wireless_reservations=[dict(start='0',end='151/500000')],wireless_attempts=[dict(received=True,feedback_known=True,outcome='success',attempt=1,end='151/500000',service=dict(data_ppdu={},mac_ack_ppdu={},radio_transmit_seconds='63/250000',reserved_service_seconds='151/500000',access_idle_seconds='17/500000',ip_bytes=1228,data_psdu_bytes=1264,mac_ack_psdu_bytes=14))])


class AirtimeReportTests(unittest.TestCase):
    def test_complete_layers_and_wireless_dispatch(self):
        r=fixture();before=copy.deepcopy(r);v=ledger(r)['complete_success_phy_ledger']
        self.assertEqual(v['total_psdu'],1278)
        self.assertEqual(v['mac_llc_fcs_over_ip'],36)
        self.assertEqual(v['other_non_transmit_seconds'],'1/62500')
        text=markdown(r)
        self.assertIn(media_markdown(r).rstrip(),text)
        self.assertIn('| MAC ACK PSDU B | 14 |',text)
        self.assertIn('| RF 发射 s | 63/250000 |',text)
        self.assertEqual(r,before)

    def test_preamble_horizon_never_counts_future_exchange(self):
        r=fixture();r['inputs']['network']['until']='11/250000'
        r['wireless_summary']['observed_reserved_seconds']='11/250000'
        r['summary']['wan_serialized_ip_bytes_by_horizon']='0'
        r['wireless_attempts'][0].update(received=False,feedback_known=False)
        self.assertIsNone(ledger(r)['complete_success_phy_ledger'])
        text=markdown(r)
        self.assertIn('| 截止内预约占用 s | 11/250000 |',text)
        self.assertIn('| 截止内 WAN 实际 IP B | 0 |',text)
        self.assertNotIn('| RF 发射 s |',text)

    def test_failed_and_unknown_feedback_are_separate(self):
        r=fixture();r['wireless_attempts'][0].update(outcome='mac_ack_lost',feedback_known=False)
        self.assertEqual(ledger(r)['known_failures'],0)
        self.assertIsNone(ledger(r)['complete_success_phy_ledger'])
        r['wireless_attempts'][0]['feedback_known']=True
        self.assertEqual(ledger(r)['known_failures'],1)
        self.assertIn('完整成功 PHY 账不可用',markdown(r))

    def test_teaching_does_not_invent_rf(self):
        r=fixture();r['wireless_attempts'][0]['service'].update(data_ppdu=None,mac_ack_ppdu=None,radio_transmit_seconds=None)
        self.assertIsNone(ledger(r)['complete_success_phy_ledger'])
        self.assertNotIn('| RF 发射 s |',markdown(r))

    def test_disabled_report_is_byte_identical(self):
        r=fixture()
        for k in ['wireless_attempts','wireless_reservations','wireless_summary']:del r[k]
        self.assertEqual(markdown(r),media_markdown(r))

    def test_reservation_before_data_start_has_no_complete_ledger(self):
        r=fixture();r['wireless_attempts']=[];r['wireless_reservations'][0]['end']=None
        self.assertIsNone(ledger(r)['complete_success_phy_ledger'])


if __name__=='__main__':unittest.main()
