import cv2 as cv
import os

def initialize_video_capture(video_path):
    """Initialize video capture from file or webcam."""
    try:
        cap = cv.VideoCapture(0 if video_path == 0 else video_path)
        if not cap.isOpened():
            raise ValueError("Couldn't open the video source.")
        return cap
    except ValueError as e:
        print(e)
        return None

def setup_video_writer(cap, output_path, resizing_factor):
    """Set up the VideoWriter object for saving compressed videos."""
    try:
        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) * resizing_factor)
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) * resizing_factor)
        frame_rate = cap.get(cv.CAP_PROP_FPS)
        fourcc = cv.VideoWriter_fourcc(*"XVID")
        return cv.VideoWriter(output_path, fourcc, frame_rate, (frame_width, frame_height))
    except Exception as e:
        print(f"Error initializing video writer: {e}")
        return None

def process_video_frames(cap, out, resizing_factor):
    """Read and resize video frames, then save to output."""
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Finished processing video.")
                break
            resized_frame = cv.resize(frame, (0, 0), fx=resizing_factor, fy=resizing_factor)
            out.write(resized_frame)
            cv.imshow('Compressed Video', resized_frame)
            if cv.waitKey(1) & 0xFF == ord('p'):
                print("Playback paused by user.")
                break
    except Exception as e:
        print(f"Error during frame processing: {e}")

def compress_video(video_path, filename, resizing_factor):
    """Compress video by resizing and saving with specified codec."""
    cap = initialize_video_capture(video_path)
    if cap is None:
        return

    video_dir = "D:\\VS CODE FILES\\OpenCV\\VIDEOS\\COMPRESSED VIDEOS"
    os.makedirs(video_dir, exist_ok=True)
    output_path = os.path.join(video_dir, filename)

    out = setup_video_writer(cap, output_path, resizing_factor)
    if out is None:
        cap.release()
        return

    process_video_frames(cap, out, resizing_factor)

    cap.release()
    out.release()
    cv.destroyAllWindows()

# Example usage:
compress_video("VIDEOS/ORIGINAL_VIDEOS/cars_on_highway.mp4", 'compressed_vid_0.5', 0.5)

