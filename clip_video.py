from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import concatenate_videoclips, VideoFileClip
from search_keywords import search_keywords 
from typing import List, Tuple
import uuid

def clip_video(video_path, start_time, end_time, output_path):
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)

def create_summary(keyword):
    results: List[Tuple[str, float, float]] = search_keywords(keyword)
    results = search_keywords(keyword)
    
    clips = []
    
    for sentence, start_time, end_time in results:
        clip_name = f"{start_time}_{end_time}.mp4"
        clip_video("original_video.mp4", float(start_time), float(end_time), clip_name)
        
        clips.append(VideoFileClip(clip_name))
        
    final_clip = concatenate_videoclips(clips)
    
    summary_filename = f"summary_{uuid.uuid4().hex}.mp4"

    final_clip.write_videofile("static/summary.mp4")

    return summary_filename