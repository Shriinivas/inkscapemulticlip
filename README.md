# Multi-clip Image Extension for Inkscape

<p align="center">
  <img src="https://github.com/Shriinivas/etc/blob/master/inkscapemulticlip/horse.gif" alt="Demo"/>
</p>

The Multi-clip Image extension for Inkscape allows users to use selected shapes to create clipping regions on a selected image. This extension adds functionality to manipulate images with various clipping paths, optionally delete the clipping paths, group clipped parts, add them below the path, and even animate the clipping results.

## Installation

To install the Multi-clip Image extension, follow these steps:

1. **Download the Extension**: Clone this repository or download the ZIP file and extract its contents.
2. **Locate Your Inkscape Extensions Directory**:
   - You will find this in the 'User Extensions' option under the System section at Edit-Preferences in Inkscape.
3. **Copy Files**: Copy the `multiclip.inx` and `multiclip.py` files into your Inkscape extensions directory.
4. **Restart Inkscape**: Close and reopen Inkscape to load the new extension.

## Usage

To use the Multi-clip Image extension:

1. **Open Inkscape**: Start Inkscape and open your project.
2. **Select Elements**:
   - Select the image you want to clip.
   - Hold down `Shift` and select the shapes that will define the clipping regions.
   - The position of image and the shapes in the layer don't matter, all the shape regions are applied to the first image within the selection
3. **Activate the Extension**:
   - Navigate to `Extensions` > `Generate from Path` > `Multi-clip Image` to open the extension dialog.
4. **Configure Options**:
   - Set the options according to your needs (detailed below).
   - Click `Apply` to perform the clipping operation.

## Options

- **Delete Selection**: If checked, the selected shapes used for clipping will be deleted after the operation.
- **Group with Shape**: If enabled, each clipped part of the image will be grouped with the corresponding shape used for clipping. This option is ignored if 'Delete Selection' is checked.
- **Add Below**: If enabled, the clipped image will be added below the path in the document's layer stack. This option is ignored if 'Delete Selection' is checked.
- **Animate**: Adds a simple SVG translation animation to each clipped part, moving it from a random position to its current position. This feature can only be observed when the SVG is viewed in a browser.

## [Video Tutorial](https://youtu.be/2XEb5q-T2xY)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
