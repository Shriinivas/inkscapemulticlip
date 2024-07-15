# Multi-clip Extension for Inkscape

<p align="center">
  <img src="https://github.com/Shriinivas/etc/blob/master/inkscapemulticlip/horse.gif" alt="Demo"/>
</p>

The Multi-clip extension for Inkscape allows users to apply the top selected objects as clipping regions on the lowest object (target) within the selection. It also has options to delete the clipping objects, group them, add them below the target, and animate the clipped results.

## Installation

To install the Multi-clip extension, follow these steps:

1. **Locate Your Inkscape Extensions Directory**:
   - You will find this in the 'User Extensions' option under the System section at Edit-Preferences in Inkscape.
2. **Download the Extension**: Download the ZIP file and extract `multiclip.inx` and `multiclip.py` files into your Inkscape extensions directory.
3. **Restart Inkscape**: Close and reopen Inkscape to load the new extension.

## Usage

To use the Multi-clip extension:

1. **Open Inkscape**: Start Inkscape and open your project.
2. **Select Elements**:
   - Make sure the target object is placed lowest in the selection (you can select just the target and press Page Down multiple times to make sure it's placed below all the clipping objects)
   - Select the target and clipping objects
3. **Activate the Extension**:
   - Navigate to `Extensions` > `Generate from Path` > `Multi-clip` to open the extension dialog.
4. **Configure Options**:
   - Set the options according to your needs (details below).
   - Click `Apply` to perform the clipping operation.

## Options

- **Delete Clipping Objects**: Uncheck this to keep the clipping objects after applying the clipping.
- **Grouping**: Select 'Group with Target Part' or 'Keep Separate' to group or not group the clipping object with target part; this is considered only if 'Delete Clipping Objects' is unchecked.
- **Clipping Object Position**: Select 'Below' or 'Above' to place the clipping object above or below the target part; this is considered only if 'Delete Clipping Objects' is unchecked.
- **Animate**: Adds a simple SVG translation animation to each clipped part, moving it from a random position to its current position. This feature can only be observed when the SVG is viewed in a browser.

## [Video Tutorial](https://youtu.be/2XEb5q-T2xY)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
