"""Values that are defined by the midi file standard.
"""


ALLOWED_MIDI_CHANNEL_TUPLE = tuple(range(16))
"""midi channels that are allowed (following the standard
midi file definition)."""

MAXIMUM_MICROSECONDS_PER_BEAT = 16777215

MIDI_TEMPO_FACTOR = 1000000
"""factor to multiply beats-in-seconds to get
beats-in-microseconds (which is the tempo unit for midi)"""

NEUTRAL_PITCH_BEND = 8191
"""the value for midi pitch bend when the resulting pitch
doesn't change"""

MAXIMUM_PITCH_BEND = 16382
"""the highest allowed value for midi pitch bend"""

MidiNote = int
"""MidiNote type alias"""

PitchBend = int
"""PitchBend type alias"""

MidiPitch = tuple[MidiNote, PitchBend]
"""MidiPitch type alias"""

MidiVelocity = int
"""MidiVelocity type alias"""
