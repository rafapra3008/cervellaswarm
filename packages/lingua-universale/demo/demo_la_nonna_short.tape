# VHS Tape File - La Nonna Demo (Short GIF for README)
# Lingua Universale: the first programming language native to AI
#
# Compact GIF at 5x speed for README embedding.
# For full version, use demo_la_nonna.tape instead.
#
# Run: cd packages/lingua-universale && vhs demo/demo_la_nonna_short.tape

Output demo/demo_la_nonna.gif

Require lu

Set Shell "zsh"
Set Theme "Catppuccin Frappe"
Set FontSize 13
Set FontFamily "JetBrains Mono"
Set Width 700
Set Height 450
Set Padding 10
Set WindowBar Colorful
Set WindowBarSize 25
Set BorderRadius 6
Set TypingSpeed 20ms
Set Framerate 6
Set PlaybackSpeed 5.0

# Brief pause
Sleep 200ms

# Type the command
Type "lu demo --lang it --speed fast"
Sleep 100ms
Enter

# Wait for demo to complete (~63s real, ~13s at 5x playback)
Sleep 70s
