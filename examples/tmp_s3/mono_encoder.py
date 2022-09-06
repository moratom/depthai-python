#!/usr/bin/env python3

import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
encodeMono = pipeline.create(dai.node.VideoEncoder)

encodeMonoOut = pipeline.create(dai.node.XLinkOut)

encodeMonoOut.setStreamName('encodeMonoOut')

# Properties
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
# Create encoders, one for each camera, consuming the frames and encoding them using H.264 / H.265 encoding
encodeMono.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H264_MAIN)

# Linking
monoLeft.out.link(encodeMono.input)
encodeMono.bitstream.link(encodeMonoOut.input)

# Connect to device and start pipeline
# device_info = dai.DeviceInfo("192.168.32.235")
with dai.Device(pipeline) as dev:

    # Output queues will be used to get the encoded data from the outputs defined above
    encoderQueue = dev.getOutputQueue(name='encodeMonoOut', maxSize=30, blocking=True)

    # The .h264 / .h265 files are raw stream files (not playable yet)
    with open('mono1.h264', 'wb') as fileMono1H264:
        print("Press Ctrl+C to stop encoding...")
        while True:
            try:
                # Empty each queue
                while encoderQueue.has():
                    encoderQueue.get().getData().tofile(fileMono1H264)
            except KeyboardInterrupt:
                # Keyboard interrupt (Ctrl + C) detected
                break

    print("To view the encoded data, convert the stream file (.h264/.h265) into a video file (.mp4), using commands below:")
    cmd = "ffmpeg -framerate 30 -i {} -c copy {}"
    print(cmd.format("mono1.h264", "mono1.mp4"))