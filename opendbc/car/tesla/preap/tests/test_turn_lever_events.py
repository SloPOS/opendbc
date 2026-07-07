"""Turn-signal lever -> ButtonEvent emission (tap detection source).

The indicator lamp (BC_indicatorLStatus) latches ON while openpilot drives the
blinker via DAS_bodyControls, so driver taps are invisible to lamp-based edge
detection. desire_helper instead consumes leftBlinker/rightBlinker ButtonEvents
built from the lever signal (STW_ACTN_RQ.TurnIndLvr_Stat). These tests pin the
lever->event transition logic.
"""
from opendbc.car import structs
from opendbc.car.tesla.preap.carstate import turn_lever_button_events

ButtonType = structs.CarState.ButtonEvent.Type


def _types(events):
  return [(be.type, be.pressed) for be in events]


def test_idle_to_left_emits_pressed():
  assert _types(turn_lever_button_events(0, 1)) == [(ButtonType.leftBlinker, True)]


def test_idle_to_right_emits_pressed():
  assert _types(turn_lever_button_events(0, 2)) == [(ButtonType.rightBlinker, True)]


def test_left_release_emits_released():
  assert _types(turn_lever_button_events(1, 0)) == [(ButtonType.leftBlinker, False)]


def test_no_change_emits_nothing():
  assert turn_lever_button_events(0, 0) == []
  assert turn_lever_button_events(1, 1) == []
  assert turn_lever_button_events(2, 2) == []


def test_sna_treated_as_idle():
  assert turn_lever_button_events(3, 0) == []
  assert _types(turn_lever_button_events(3, 1)) == [(ButtonType.leftBlinker, True)]
  assert _types(turn_lever_button_events(1, 3)) == [(ButtonType.leftBlinker, False)]


def test_direct_left_to_right_emits_both():
  evs = _types(turn_lever_button_events(1, 2))
  assert (ButtonType.leftBlinker, False) in evs
  assert (ButtonType.rightBlinker, True) in evs
  assert len(evs) == 2
