"""
search_keywords 에서 반환된 시작 시간 및 종료 시간에 따라 원본 비디오에서 해당 부분을 잘라내어 새로운 클립들을 생성. 
그 후 모든 클립들을 하나의 최종 요약 비디오로 합침. 
"""
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import concatenate_videoclips, VideoFileClip
from search_keywords import search_keywords 
from typing import List, Tuple
import uuid
import os
from flask import session

def clip_video(video_path, start_time, end_time, output_path):
    ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)

def create_summary(keyword):
    results: List[Tuple[str, float, float]] = search_keywords(keyword)
    results = search_keywords(keyword)
    
    clips = []
    
    for sentence, start_time, end_time in results:
        clip_name = f"{start_time}_{end_time}.mp4"
        clip_path = os.path.join("static", clip_name) 

        clip_video(session.get('video_filepath'), float(start_time), float(end_time), clip_path)
        
        clips.append(VideoFileClip(clip_path))
        
    final_clip = concatenate_videoclips(clips)
    
    summary_filename = f"summary_{uuid.uuid4().hex}.mp4"
    summary_path = os.path.join("static", summary_filename) 

    final_clip.write_videofile("static/summary.mp4")

    return summary_filename