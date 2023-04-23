import pyrealsense2 as rs

pipe = rs.pipeline()
pipe.start()

images = []
counter = 0
while counter < 5:
    frames = pipe.wait_for_frames()
    image = frames.get_color_frame()
    images.append(image)

    counter += 1

pipe.stop()