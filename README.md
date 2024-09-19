# BeamNG glTF Sequence Importer

Blender add-on for importing glTF sequences from BeamNG.drive.

This addon is intended for use with my BeamNG.drive mod [glTF Sequence Exporter](https://github.com/oli-caon/beamng-gltf-sequence-exporter).

## Installation

Download `beamng_gltf_sequence_importer-0.1.0.zip` the [latest release](https://github.com/oli-caon/beamng-gltf-sequence-importer/releases) and install it in the Blender preferences as an add-on.

## Usage

In the Blender menu choose
`File > Import > BeamNG glTF Sequence`.

Select one of your sequence files and choose a name for the sequence. It can take a while to finish importing long sequences and Blender may freeze during the process.

The imported frames are stored in a collection and an object is created to instance the current frame using a Geometry Nodes modifier.

## Limitations

The materials will usually need some cleanup as they aren't imported exactly how they appear in-game, especially for glass and mirrors.

There may be some z-fighting on number plates because they are modeled as two planes. You can fix this with backface culling or by editing the geometry.
