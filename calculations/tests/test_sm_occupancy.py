import unittest
from _gap_common import scenario_rows
from infra_calc.topics.sm_occupancy import calculate


class SMOccupancyTests(unittest.TestCase):
    def test_book_tile_binding_limits(self):
        r = calculate()
        self.assertEqual(r['block']['shared_bytes_per_block'], 96 * 1024)
        self.assertEqual(r['block']['gemm_tiles_reserved_working_bytes'], 96 * 1024)
        self.assertEqual(r['residency']['blocks_by_limit'], dict(threads=8, registers=2, shared_memory=2, blocks=32))
        self.assertEqual(r['residency']['occupancy_exact'], '1/4')
        self.assertEqual(r['mma']['instructions_per_tile'], 512)
        self.assertEqual(r['mma']['instructions_per_tile'] * r['mma']['flops_per_instruction'], 2 * 128 * 128 * 64)
        lh = r['latency_hiding']
        self.assertAlmostEqual(lh['needed_bytes_in_flight_gpu'], 3350e9 * 600e-9)
        self.assertEqual(lh['available_bytes_in_flight_per_sm'], 16 * 4 * 32 * 16)

    def test_register_accumulator_and_validation(self):
        r = calculate(accumulator_in_shared=False, declared_registers_per_thread=64)
        self.assertEqual(r['block']['registers_per_thread'], 64 + 64)
        self.assertEqual(r['residency']['binding_limits'], ['registers'])
        with self.assertRaises(ValueError):
            calculate(threads_per_block=100)
        with self.assertRaises(ValueError):
            calculate(declared_mma_shape=(16, 8, 24))

    def test_scenarios(self):
        for row in scenario_rows('sm_occupancy'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
