"""Business/report boundaries, independent of network implementation details."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.transport.media_report import markdown


def fixture():
    return dict(inputs=dict(application=dict(scheduling={'send':'fifo','compute':'fifo'},messages=[],compute_tasks=[dict(id='model',duration_seconds='0.3')]),network=dict(until=1,controller={'name':'newreno'})),summary=dict(complete=False,all_messages_delivered=False,pending_packets={'up':0,'down':0},wire_bytes=100,serialized_wire_bytes_by_horizon='99/2',unique_received_application_bytes=10,delivered_application_bytes=0),businesses=[],transmissions=[],waits=[],message_status={})


class MediaReportTests(unittest.TestCase):
    def test_empty_queue_does_not_claim_business_success(self):
        r=fixture();r['businesses']=[dict(id='image',kind='image',complete=False,all_required_delivered=False,complete_at=None,missing=['tail'])]
        text=markdown(r)
        self.assertIn('全部业务完成（结果标志）：**否**',text)
        self.assertIn('队列为空不等于业务成功',text)
        self.assertIn('| image | 否 | 否 | 未完成／无记录',text)
        self.assertIn('观察期内实际序列化字节：99/2B',text)

    def test_partial_play_has_separate_scheduled_and_actual_end(self):
        r=fixture();r['businesses']=[dict(id='audio',kind='tts',complete=False,all_required_delivered=True,complete_at='0.2',missing=[],first_play='0.5',playback_end=None,stall_seconds=0,missing_audio_seconds=0,blocks=[dict(arrival='0.2',play_start='0.5',scheduled_play_end='1.5',play_end=None)])]
        text=markdown(r)
        self.assertIn('实际播放结束 未完成／无记录',text)
        self.assertIn('已开始 1/1 块，已播放结束 0/1 块',text)
        self.assertIn('| 1 | 0.2s | 0.5s | 1.5s | 未完成／无记录 |',text)

    def test_ack_loss_and_delivered_stale_screenshot_remain_distinct(self):
        r=fixture();r['businesses']=[dict(id='screen',kind='screenshot',complete=True,all_required_delivered=True,complete_at='0.8',usable=False,expected_version='v1',version_at_result='v2',missing=[])]
        r['transmissions']=[dict(direction='up',pn=0,kind='ack',frames=[],wire_bytes=92,dropped=False,probe=False,recovery_of=None)]
        r['losses']={'up':[dict(pn=0,at=1)]}
        text=markdown(r)
        self.assertIn('传输身份：纯 ACK 1',text)
        self.assertNotIn('STREAM 数据 1',text)
        self.assertIn('| screen | 是 | 是 | 0.8s | 否 |',text)

    def test_report_is_bounded_and_does_not_mutate_inputs(self):
        r=fixture();r['inputs']['application']['messages']=[{'id':str(i)} for i in range(1420)]
        r['message_status']={str(i):'waiting' for i in range(1420)}
        r['waits']=[dict(reasons=['cwnd','MAX_STREAM_DATA:A']) for _ in range(20)]
        before=copy.deepcopy(r);text=markdown(r)
        self.assertEqual(r,before)
        self.assertLess(len(text),12000)
        self.assertIn('不是累计等待时长',text)
        self.assertIn('| MAX_STREAM_DATA:A | 20 |',text)
        self.assertIn('输入假设，不是实测',text)


if __name__=='__main__':unittest.main()
