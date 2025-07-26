import json
import os
from pathlib import Path

class LessonManager:
    def __init__(self):
        self.lessons_dir = Path("lessons")
        self.progress_file = Path("progress.json")
        self.progress_data = self.load_progress()
        self.available_lessons = self.scan_available_lessons()
    
    def load_progress(self):
        """Load user progress from file"""
        try:
            if self.progress_file.exists():
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.create_default_progress()
        except (json.JSONDecodeError, IOError):
            print("Error loading progress file, creating new one.")
            return self.create_default_progress()
    
    def create_default_progress(self):
        """Create default progress data"""
        return {
            "last_completed_lesson": 0,
            "completed_lessons": [],
            "current_lesson": 1,
            "total_lessons_available": 1
        }
    
    def save_progress(self):
        """Save current progress to file"""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving progress: {e}")
    
    def scan_available_lessons(self):
        """Scan lessons directory and return available lesson info"""
        if not self.lessons_dir.exists():
            print("Lessons directory not found. Creating it...")
            self.lessons_dir.mkdir(exist_ok=True)
            return []
        
        lessons = []
        for lesson_file in sorted(self.lessons_dir.glob("lesson_*.json")):
            try:
                with open(lesson_file, 'r', encoding='utf-8') as f:
                    lesson_data = json.load(f)
                    lessons.append({
                        "number": lesson_data.get("lesson_number", 0),
                        "title": lesson_data.get("lesson_title", "Unknown"),
                        "file": lesson_file
                    })
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error reading {lesson_file}: {e}")
        
        # Update total available lessons in progress
        self.progress_data["total_lessons_available"] = len(lessons)
        return lessons
    
    def get_lesson_info(self, lesson_number):
        """Get basic info about a lesson without loading full content"""
        for lesson in self.available_lessons:
            if lesson["number"] == lesson_number:
                return lesson
        return None
    
    def load_lesson(self, lesson_number):
        """Load full lesson content"""
        lesson_file = self.lessons_dir / f"lesson_{lesson_number:02d}.json"
        
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading lesson {lesson_number}: {e}")
            return None
    
    def mark_lesson_completed(self, lesson_number):
        """Mark a lesson as completed"""
        if lesson_number not in self.progress_data["completed_lessons"]:
            self.progress_data["completed_lessons"].append(lesson_number)
            self.progress_data["completed_lessons"].sort()
        
        self.progress_data["last_completed_lesson"] = max(
            self.progress_data["last_completed_lesson"], 
            lesson_number
        )
        self.save_progress()
    
    def is_lesson_completed(self, lesson_number):
        """Check if a lesson is completed"""
        return lesson_number in self.progress_data["completed_lessons"]
    
    def get_next_lesson(self):
        """Get the next lesson number to study"""
        return self.progress_data["last_completed_lesson"] + 1
    
    def get_current_lesson(self):
        """Get currently selected lesson"""
        return self.progress_data.get("current_lesson", 1)
    
    def set_current_lesson(self, lesson_number):
        """Set current lesson"""
        self.progress_data["current_lesson"] = lesson_number
        self.save_progress()
    
    def get_available_lessons(self):
        """Get list of all available lessons"""
        return self.available_lessons
    
    def get_progress_summary(self):
        """Get summary of user progress"""
        total_lessons = len(self.available_lessons)
        completed_count = len(self.progress_data["completed_lessons"])
        
        return {
            "total_lessons": total_lessons,
            "completed_lessons": completed_count,
            "completion_percentage": (completed_count / total_lessons * 100) if total_lessons > 0 else 0,
            "last_completed": self.progress_data["last_completed_lesson"],
            "next_lesson": self.get_next_lesson()
        }