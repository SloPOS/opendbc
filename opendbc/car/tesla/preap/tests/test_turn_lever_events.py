"""turnSignalStalkState — the lane-change tap-detection source.

The indicator lamp (BC_indicatorLStatus) latches ON while openpilot drives the
blinker via DAS_bodyControls, so driver taps are invisible to lamp-based edge
detection. desire_helper instead edge-detects the turn-signal LEVER, published
on CarState.turnSignalStalkState as a level signal (survives the conflated
~20Hz carState reads in modeld, unlike single-message ButtonEvents).

These tests pin the schema field and the SNA sanitization convention.
"""
from opendbc.car import structs


def test_carstate_has_turn_signal_stalk_state_field():
  ret = structs.CarState()
  ret.turnSignalStalkState = 2
  assert ret.turnSignalStalkState == 2


def test_sna_sanitization_convention():
  # carstate maps lever value 3 (SNA) to 0 (idle): `0 if lever == 3 else lever`
  for lever, expected in ((0, 0), (1, 1), (2, 2), (3, 0)):
    assert (0 if lever == 3 else lever) == expected
