# BeamNG glTF Sequence Importer

Blender add-on for importing glTF sequences from BeamNG.drive.

This addon is intended for use with my BeamNG.drive mod [glTF Sequence Exporter](https://github.com/oli-caon/beamng-gltf-sequence-exporter).

## Installation

This add-on is only supported for Blender 4.2.

Download the [latest release](https://github.com/oli-caon/beamng-gltf-sequence-importer/releases) and drag and drop the .zip file into Blender to install. You can also install the .zip file through the Blender preferences via "Get Extensions -> Install from Disk..." or "Add-ons -> Install from Disk...".

## Usage

In the Blender menu choose
`File > Import > BeamNG glTF Sequence`.

Select one of your sequence files and choose a name for the sequence. It can take a while to finish importing long sequences and Blender may freeze during the process. You can enable Blender's system console with "Window -> Toggle System Console" before importing to keep an eye on the progress if it freezes.

The imported frames are stored in a collection and an object is created to instance the current frame using a Geometry Nodes modifier.

## Limitations

The materials will usually need some cleanup as they aren't imported exactly how they appear in-game, especially for glass and mirrors.

There may be some z-fighting on number plates because they are modeled as two planes. You can fix this with backface culling or by editing the geometry.
