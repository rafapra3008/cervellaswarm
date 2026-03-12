# VHS Tape File - La Nonna Demo (Full Version)
# Lingua Universale: the first programming language native to AI
#
# Full demo: ~70s at slow speed. Produces MP4 for YouTube.
# For README GIF, use demo_la_nonna_short.tape instead.
#
# Run: cd packages/lingua-universale && vhs demo/demo_la_nonna.tape

Output demo/demo_la_nonna.mp4

Require lu

Set Shell "zsh"
Set Theme "Catppuccin Frappe"
Set FontSize 16
Set FontFamily "JetBrains Mono"
Set Width 1200
Set Height 700
Set Padding 20
Set WindowBar Colorful
Set WindowBarSize 40
Set BorderRadius 8
Set TypingSpeed 60ms
Set Framerate 30

# Title card: brief pause before starting
Sleep 1s

# Type the command to run the demo
Type "lu demo --lang it --speed slow"
Sleep 500ms
Enter

# The demo runs autonomously with typewriter effect (~68s at slow speed)
# Wait for it to complete + 5s final pause
Sleep 75s
