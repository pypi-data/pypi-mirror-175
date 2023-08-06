# Trace Extractor

A wrapper around ffprobe that takes MPEG-4 files and outputs video traces in a format readable by [ns-3](https://gitlab.com/nsnam/ns-3-dev)'s UdpTraceClient application.

## Dependencies

You need to have [ffmpeg](https://ffmpeg.org/)'s `ffprobe` present in your `PATH`. Alternatively, you can use a custom `ffprobe` with the `--ffprobe-path` argument:

```
python3 -m trace_extractor --ffprobe-path /path/to/ffprobe
```

## Installation

`trace_extractor` can be installed via `pip`:

```
pip install trace-extractor
```

## Usage

To run the program, you need to specify the MP4 file you wish to process and the path to the output file.

```
python3 -m trace_extractor -i path/to/input.mp4 -o path/to/output.ns-3-vtrace
```

## Example

An example video is present in the `tests/inputs` directory, it is a recording of id Software's 1993 DOOM's DEMO1 demo played back on the [dsda-doom](https://github.com/kraflab/dsda-doom) source port.
