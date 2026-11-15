import os
import sys
from unittest import TestCase

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from shared.partial_integer import PartialInteger


class TestPartialInteger(TestCase):
    def test_add_known(self):
        p = PartialInteger().add_known(0b1010, 4)
        self.assertEqual(p.bit_length, 4)
        self.assertEqual(p.unknowns, 0)
        self.assertEqual(p.to_int(), 0b1010)
        self.assertIs(p.add_known(0b11, 2), p)

    def test_add_unknown(self):
        p = PartialInteger().add_unknown(8)
        self.assertEqual(p.bit_length, 8)
        self.assertEqual(p.unknowns, 1)
        self.assertEqual(p.get_unknown_bounds(), [256])
        self.assertIs(p.add_unknown(4), p)

    def test_get_known_lsb(self):
        # 10??011 read msb first: known lsb run is 011.
        p = PartialInteger.from_bits_be("10??011")
        self.assertEqual(p.get_known_lsb(), (0b011, 3))

    def test_get_known_lsb_stops_at_unknown(self):
        p = PartialInteger.from_bits_be("101?")
        self.assertEqual(p.get_known_lsb(), (0, 0))

    def test_get_known_msb(self):
        p = PartialInteger.from_bits_be("10??011")
        self.assertEqual(p.get_known_msb(), (0b10, 2))

    def test_get_known_msb_stops_at_unknown(self):
        p = PartialInteger.from_bits_be("?101")
        self.assertEqual(p.get_known_msb(), (0, 0))

    def test_get_known_middle(self):
        # Leading unknowns are skipped, so the known middle run is 101.
        p = PartialInteger.from_bits_be("??101??")
        self.assertEqual(p.get_known_middle(), (0b101, 3))

    def test_get_unknown_lsb(self):
        p = PartialInteger.from_bits_be("101??")
        self.assertEqual(p.get_unknown_lsb(), 2)

    def test_get_unknown_lsb_stops_at_known(self):
        p = PartialInteger.from_bits_be("1??01")
        self.assertEqual(p.get_unknown_lsb(), 0)

    def test_get_unknown_msb(self):
        p = PartialInteger.from_bits_be("??011")
        self.assertEqual(p.get_unknown_msb(), 2)

    def test_get_unknown_msb_stops_at_known(self):
        p = PartialInteger.from_bits_be("10?11")
        self.assertEqual(p.get_unknown_msb(), 0)

    def test_matches(self):
        p = PartialInteger.from_bits_be("10??011")
        self.assertTrue(p.matches(0b1000011))
        self.assertTrue(p.matches(0b1011011))
        self.assertFalse(p.matches(0b0000011))
        self.assertFalse(p.matches(0b1000010))

    def test_sub(self):
        p = PartialInteger.from_bits_be("10??011")
        self.assertEqual(p.sub([0b01]), 0b1001011)
        self.assertEqual(p.sub([0b11]), 0b1011011)

    def test_get_known_and_unknowns(self):
        p = PartialInteger.from_bits_be("10??011")
        self.assertEqual(p.get_known_and_unknowns(), (0b1000011, [3], [2]))

    def test_get_unknown_bounds(self):
        p = (PartialInteger().add_known(0b11, 2).add_unknown(3)
             .add_known(0b101, 3).add_unknown(1).add_known(0b0, 1))
        self.assertEqual(p.get_unknown_bounds(), [8, 2])

    def test_to_int(self):
        self.assertEqual(PartialInteger().add_known(0b1010, 4).to_int(), 10)

    def test_to_int_requires_no_unknowns(self):
        with self.assertRaises(AssertionError):
            PartialInteger.from_bits_be("10??011").to_int()

    def test_to_bits_le(self):
        p = PartialInteger.from_bits_be("10??011")
        self.assertEqual("".join(p.to_bits_le()), "110??01")

    def test_to_bits_be(self):
        p = PartialInteger.from_bits_le("110??01")
        self.assertEqual("".join(p.to_bits_be()), "10??011")

    def test_to_hex_be(self):
        self.assertEqual("".join(PartialInteger.from_hex_be("12?4abc").to_hex_be()), "12?4abc")

    def test_to_string_le_requires_power_of_two_base(self):
        with self.assertRaises(AssertionError):
            PartialInteger.from_bits_be("101").to_string_le(10)

    def test_parse_le(self):
        self.assertEqual(PartialInteger.parse_le("ff", 16).to_int(), 255)
        self.assertEqual("".join(PartialInteger.parse_le("?f", 16).to_bits_be()), "1111????")

    def test_parse_le_accepts_none(self):
        self.assertEqual("".join(PartialInteger.parse_le(["a", None, "c"], 16).to_bits_be()), "1100????1010")

    def test_parse_be(self):
        # Big endian input must be reversed before parsing as little endian.
        p = PartialInteger.parse_be("12?4abc", 16)
        self.assertEqual("".join(p.to_hex_be()), "12?4abc")

    def test_from_bits_be(self):
        self.assertEqual(PartialInteger.from_bits_be("101").to_int(), 0b101)
        self.assertEqual("".join(PartialInteger.from_bits_le("101").to_bits_be()), "101")

    def test_unknown(self):
        self.assertEqual("".join(PartialInteger.unknown(5).to_bits_be()), "?????")

    def test_from_lsb(self):
        p = PartialInteger.from_lsb(32, 0xBEEF, 16)
        self.assertEqual(p.bit_length, 32)
        self.assertEqual(p.get_known_lsb(), (0xBEEF, 16))
        self.assertEqual(p.get_unknown_msb(), 16)

    def test_from_msb(self):
        p = PartialInteger.from_msb(32, 0xBEEF, 16)
        self.assertEqual(p.get_known_msb(), (0xBEEF, 16))
        self.assertEqual(p.get_unknown_lsb(), 16)

    def test_from_lsb_and_msb(self):
        p = PartialInteger.from_lsb_and_msb(32, 0xBEEF, 16, 0x1234, 16)
        self.assertEqual(p.get_known_lsb(), (0xBEEF, 16))
        self.assertEqual(p.get_known_msb(), (0x1234, 16))
        self.assertEqual(p.get_unknown_bounds(), [1])

    def test_from_middle(self):
        p = PartialInteger.from_middle(0b101, 3, 2, 3)
        self.assertEqual("".join(p.to_bits_be()), "???101??")
        self.assertEqual(p.get_known_middle(), (0b101, 3))

    def test_lsb_of(self):
        p = PartialInteger.lsb_of(0b1111010111, 10, 4)
        self.assertEqual(p.get_known_lsb(), (0b0111, 4))
        self.assertEqual(p.bit_length, 10)

    def test_msb_of(self):
        p = PartialInteger.msb_of(0b1111010111, 10, 4)
        self.assertEqual(p.get_known_msb(), (0b1111, 4))
        self.assertEqual(p.bit_length, 10)

    def test_lsb_and_msb_of(self):
        self.assertEqual("".join(PartialInteger.lsb_and_msb_of(0b1111010111, 10, 4, 4).to_bits_be()), "1111??0111")

    def test_middle_of(self):
        self.assertEqual("".join(PartialInteger.middle_of(0b1111010111, 10, 2, 3).to_bits_be()), "???10101??")
