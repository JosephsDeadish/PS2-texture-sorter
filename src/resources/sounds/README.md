# Sound Files

This directory contains WAV audio files for the PS2 Texture Sorter application.

## File Organization

### System Sounds
- `complete*.wav` - Task completion sounds (7 variants)
- `error*.wav` - Error notification sounds (6 variants)
- `achievement*.wav` - Achievement unlock sounds (5 variants)
- `milestone*.wav` - Milestone reached sounds (3 variants)
- `warning*.wav` - Warning notification sounds (3 variants)
- `start*.wav` - Process start sounds (4 variants)
- `pause*.wav` - Pause sounds (2 variants)
- `resume*.wav` - Resume sounds (2 variants)
- `stop*.wav` - Stop sounds (2 variants)
- `click*.wav` - Button click sounds (6 variants)
- `notification*.wav` - Notification sounds (5 variants)

### Panda Sounds
- `panda_*` - Various panda interaction sounds (48 variants)
  - Eating: munch, chomp, nom, crunch, slurp
  - Happy: chirp, purr, squeal, giggle
  - Sad: whimper, sigh, cry
  - Movement: slide, drag whoosh, shuffle, thud, bounce, plop
  - Sleep: snore, zzz, breath, wake yawn, stretch
  - Interaction: boop, poke, squeak, pet purr
  - Activity: playful, excited, energetic, pitter, boing, dance
  - Other: sneeze, yawn variants

## Sound Generation

Most of these sounds are synthetically generated using various waveforms:

- **Sine waves**: Smooth, musical tones (bells, chimes)
- **Square waves**: Harsh, buzzy tones (alarms, buzzes)
- **Sawtooth waves**: Buzzy but smoother (alerts)
- **Triangle waves**: Organic sounds (purrs, breaths)
- **Frequency sweeps**: Whooshes and dynamic effects
- **Chord combinations**: Rich, layered sounds

All sounds use ADSR envelopes (Attack, Decay, Sustain, Release) for realistic sound shaping.

## File Format

- **Format**: WAV (PCM)
- **Sample Rate**: 44100 Hz
- **Bit Depth**: 16-bit
- **Channels**: Mono (1 channel)

## Usage

Sounds are selected via the Sound Settings panel in Advanced Customization. Each event type has multiple sound variants to choose from.

To regenerate or add new sounds, run `generate_sounds.py` from the repository root.

## Customization

You can replace any WAV file with your own custom sounds. Make sure they match the naming convention and are in the correct format (44100 Hz, 16-bit, mono WAV).
