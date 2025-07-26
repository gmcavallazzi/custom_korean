import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path

class KoreanLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Learning App")
        self.root.geometry("1000x700")
        self.root.configure(bg='#ffffff')
        
        # Load lesson data
        self.current_lesson = self.load_lesson_from_file()
        self.current_exercise_index = 0
        self.current_vocab_page = 0
        self.vocab_per_page = 3
        
        # Create UI
        self.create_widgets()
        self.show_lesson_overview()
    
    def load_lesson_from_file(self, lesson_number=1):
        """Load lesson data from JSON file in lessons folder"""
        lessons_dir = Path("lessons")
        lesson_file = lessons_dir / f"lesson_{lesson_number:02d}.json"
        
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Lesson file {lesson_file} not found. Using default lesson.")
            return self.get_default_lesson()
        except json.JSONDecodeError:
            print(f"Error parsing {lesson_file}. Using default lesson.")
            return self.get_default_lesson()
    
    def get_default_lesson(self):
        """Fallback lesson if file loading fails"""
        return {
            "lesson_number": 1,
            "lesson_title": "Basic Sentence Structure and 이다/아니다",
            "grammar_rules": [],
            "vocabulary": [],
            "example_sentences": [],
            "exercises": []
        }
    
    def create_button(self, parent, text, command, style="default", **kwargs):
        """Create standardized buttons with consistent styling"""
        styles = {
            "default": {
                "font": ('Arial', 14, 'bold'),
                "bg": '#ffffff',
                "fg": '#000000',
                "activebackground": '#ffffff',
                "activeforeground": '#000000',
                "highlightbackground": '#ffffff',
                "padx": 15,
                "pady": 8,
                "relief": tk.FLAT,
                "bd": 1,
                "borderwidth": 1
            },
            "nav": {
                "font": ('Arial', 14, 'bold'),
                "bg": '#ffffff',
                "fg": '#000000',
                "activebackground": '#ffffff',
                "activeforeground": '#000000',
                "highlightbackground": '#ffffff',
                "padx": 15,
                "pady": 8,
                "relief": tk.FLAT,
                "bd": 1,
                "borderwidth": 1
            },
            "exercise": {
                "font": ('Arial', 16),
                "bg": '#f9fafb',
                "fg": '#1f2937',
                "padx": 20,
                "pady": 10,
                "relief": tk.SOLID,
                "bd": 1
            },
            "korean": {
                "font": ('Arial', 18, 'bold'),
                "bg": '#f9fafb',
                "fg": '#dc2626',
                "padx": 20,
                "pady": 10,
                "relief": tk.SOLID,
                "bd": 1
            },
            "action": {
                "font": ('Arial', 14, 'bold'),
                "bg": '#059669',
                "fg": 'white',
                "padx": 15,
                "pady": 8,
                "relief": tk.RAISED,
                "bd": 2
            },
            "danger": {
                "font": ('Arial', 14),
                "bg": '#dc2626',
                "fg": 'white',
                "padx": 15,
                "pady": 8,
                "relief": tk.RAISED,
                "bd": 2
            }
        }
        
        button_style = styles.get(style, styles["default"])
        button_style.update(kwargs)
        
        return tk.Button(parent, text=text, command=command, **button_style)
    
    def create_label(self, parent, text, style="default", **kwargs):
        """Create standardized labels with consistent styling"""
        styles = {
            "title": {
                "font": ('Arial', 24, 'bold'),
                "bg": '#ffffff',
                "fg": '#1f2937'
            },
            "subtitle": {
                "font": ('Arial', 20, 'bold'),
                "bg": '#ffffff',
                "fg": '#1f2937'
            },
            "heading": {
                "font": ('Arial', 18, 'bold'),
                "bg": '#ffffff',
                "fg": '#1f2937'
            },
            "body": {
                "font": ('Arial', 16),
                "bg": '#ffffff',
                "fg": '#374151',
                "justify": tk.LEFT
            },
            "korean": {
                "font": ('Arial', 20, 'bold'),
                "bg": '#f9fafb',
                "fg": '#dc2626'
            },
            "romanization": {
                "font": ('Arial', 14, 'italic'),
                "bg": '#f9fafb',
                "fg": '#6b7280'
            },
            "english": {
                "font": ('Arial', 16),
                "bg": '#f9fafb',
                "fg": '#1f2937'
            },
            "hint": {
                "font": ('Arial', 14, 'italic'),
                "bg": '#ffffff',
                "fg": '#6b7280'
            }
        }
        
        label_style = styles.get(style, styles["body"])
        label_style.update(kwargs)
        
        return tk.Label(parent, text=text, **label_style)
    
    def create_content_frame(self, parent, style="default", **kwargs):
        """Create standardized content frames"""
        styles = {
            "default": {
                "bg": '#ffffff'
            },
            "card": {
                "bg": '#f9fafb',
                "relief": tk.SOLID,
                "bd": 1
            }
        }
        
        frame_style = styles.get(style, styles["default"])
        frame_style.update(kwargs)
        
        return tk.Frame(parent, **frame_style)
    
    def create_widgets(self):
        # Main frame
        main_frame = self.create_content_frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Navigation buttons
        nav_frame = self.create_content_frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        nav_buttons = [
            ("Lesson Overview", self.show_lesson_overview),
            ("Vocabulary", self.show_vocabulary),
            ("Grammar", self.show_grammar),
            ("Exercises", self.show_exercises)
        ]
        
        for text, command in nav_buttons:
            btn = self.create_button(nav_frame, text, command, style="nav")
            btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Content frame
        self.content_frame = self.create_content_frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def clear_content(self):
        """Clear all widgets from content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_lesson_overview(self):
        self.clear_content()
        
        title_text = f"Lesson {self.current_lesson['lesson_number']}: {self.current_lesson['lesson_title']}"
        title = self.create_label(self.content_frame, title_text, style="title")
        title.pack(pady=(0, 30), anchor=tk.W)
        
        overview_text = f"""Lesson {self.current_lesson['lesson_number']}: {self.current_lesson['lesson_title']}

{len(self.current_lesson['vocabulary'])} vocabulary words
{len(self.current_lesson['grammar_rules'])} grammar rules  
{len(self.current_lesson['exercises'])} exercises

Click the buttons above to navigate between sections."""
        
        overview_label = self.create_label(self.content_frame, overview_text, style="body")
        overview_label.pack(anchor=tk.W)
    
    def show_vocabulary(self):
        self.clear_content()
        
        title = self.create_label(self.content_frame, "Vocabulary", style="subtitle")
        title.pack(pady=(0, 20), anchor=tk.W)
        
        # Calculate pagination
        vocab_list = self.current_lesson["vocabulary"]
        total_pages = (len(vocab_list) + self.vocab_per_page - 1) // self.vocab_per_page
        start_idx = self.current_vocab_page * self.vocab_per_page
        end_idx = min(start_idx + self.vocab_per_page, len(vocab_list))
        
        # Show page info
        page_info = self.create_label(self.content_frame, 
                                    f"Page {self.current_vocab_page + 1} of {total_pages}", 
                                    style="hint")
        page_info.pack(pady=(0, 15), anchor=tk.W)
        
        # Show vocabulary for current page
        for vocab in vocab_list[start_idx:end_idx]:
            vocab_frame = self.create_content_frame(self.content_frame, style="card")
            vocab_frame.pack(fill=tk.X, pady=10, padx=0)
            
            korean_label = self.create_label(vocab_frame, vocab["korean"], style="korean")
            korean_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
            
            rom_label = self.create_label(vocab_frame, f"[{vocab['romanization']}]", style="romanization")
            rom_label.pack(anchor=tk.W, padx=15)
            
            eng_label = self.create_label(vocab_frame, vocab["english"], style="english")
            eng_label.pack(anchor=tk.W, padx=15, pady=(0, 10))
        
        # Navigation buttons
        if total_pages > 1:
            self.create_vocab_navigation(total_pages)
    
    def create_vocab_navigation(self, total_pages):
        """Create navigation buttons for vocabulary pages"""
        nav_button_frame = self.create_content_frame(self.content_frame)
        nav_button_frame.pack(pady=20)
        
        if self.current_vocab_page > 0:
            prev_btn = self.create_button(nav_button_frame, "Previous", self.prev_vocab_page)
            prev_btn.pack(side=tk.LEFT, padx=10)
        
        if self.current_vocab_page < total_pages - 1:
            next_btn = self.create_button(nav_button_frame, "Next", self.next_vocab_page)
            next_btn.pack(side=tk.LEFT, padx=10)
    
    def prev_vocab_page(self):
        if self.current_vocab_page > 0:
            self.current_vocab_page -= 1
            self.show_vocabulary()
    
    def next_vocab_page(self):
        vocab_list = self.current_lesson["vocabulary"]
        total_pages = (len(vocab_list) + self.vocab_per_page - 1) // self.vocab_per_page
        if self.current_vocab_page < total_pages - 1:
            self.current_vocab_page += 1
            self.show_vocabulary()
    
    def show_grammar(self):
        self.clear_content()
        
        title = self.create_label(self.content_frame, "Grammar", style="subtitle")
        title.pack(pady=(0, 20), anchor=tk.W)
        
        for rule in self.current_lesson["grammar_rules"]:
            self.create_grammar_rule_display(rule)
        
        # Show example sentences
        if self.current_lesson["example_sentences"]:
            self.create_example_sentences_display()
    
    def create_grammar_rule_display(self, rule):
        """Create display for a single grammar rule"""
        rule_frame = self.create_content_frame(self.content_frame, style="card")
        rule_frame.pack(fill=tk.X, pady=10, padx=0)
        
        rule_title = self.create_label(rule_frame, rule["title"], style="heading", bg='#f9fafb')
        rule_title.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        explanation = self.create_label(rule_frame, rule["explanation"], 
                                      style="body", bg='#f9fafb', wraplength=800)
        explanation.pack(anchor=tk.W, padx=15, pady=5)
        
        pattern = self.create_label(rule_frame, f"Pattern: {rule['pattern']}", 
                                  style="hint", bg='#f9fafb')
        pattern.pack(anchor=tk.W, padx=15, pady=5)
        
        if "formality_note" in rule:
            note = self.create_label(rule_frame, f"Note: {rule['formality_note']}", 
                                   font=('Arial', 12), bg='#f9fafb', fg='#6b7280')
            note.pack(anchor=tk.W, padx=15, pady=(0, 10))
    
    def create_example_sentences_display(self):
        """Create display for example sentences"""
        examples_title = self.create_label(self.content_frame, "Example Sentences", style="heading")
        examples_title.pack(pady=(30, 15), anchor=tk.W)
        
        for example in self.current_lesson["example_sentences"]:
            example_frame = self.create_content_frame(self.content_frame, style="card")
            example_frame.pack(fill=tk.X, pady=5, padx=0)
            
            korean_label = self.create_label(example_frame, example["korean"], style="korean")
            korean_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
            
            rom_label = self.create_label(example_frame, example["romanization"], style="romanization")
            rom_label.pack(anchor=tk.W, padx=15)
            
            eng_label = self.create_label(example_frame, example["english"], style="english")
            eng_label.pack(anchor=tk.W, padx=15, pady=(0, 10))
    
    def show_exercises(self):
        self.clear_content()
        
        if self.current_exercise_index >= len(self.current_lesson["exercises"]):
            self.show_exercises_completed()
            return
        
        exercise = self.current_lesson["exercises"][self.current_exercise_index]
        
        title = self.create_label(self.content_frame, 
                                f"Exercise {self.current_exercise_index + 1} of {len(self.current_lesson['exercises'])}", 
                                style="subtitle")
        title.pack(pady=(0, 30))
        
        exercise_handlers = {
            "multiple_choice": self.show_multiple_choice_exercise,
            "syllable_choice": self.show_syllable_choice_exercise,
            "word_building": self.show_word_building_exercise
        }
        
        handler = exercise_handlers.get(exercise["type"])
        if handler:
            handler(exercise)
    
    def show_exercises_completed(self):
        """Display completion message and restart option"""
        completed_label = self.create_label(self.content_frame, "All exercises completed! Great job!", 
                                          font=('Arial', 20, 'bold'), fg='#059669')
        completed_label.pack(pady=50)
        
        restart_btn = self.create_button(self.content_frame, "Restart Exercises", 
                                       self.restart_exercises, style="action",
                                       font=('Arial', 16, 'bold'), padx=20, pady=10)
        restart_btn.pack(pady=20)
    
    def show_multiple_choice_exercise(self, exercise):
        question_label = self.create_label(self.content_frame, exercise["question"], style="body")
        question_label.pack(pady=(0, 20))
        
        for i, option in enumerate(exercise["options"]):
            btn = self.create_button(self.content_frame, option,
                                   lambda idx=i: self.check_multiple_choice(exercise, idx),
                                   style="exercise")
            btn.pack(pady=5, fill=tk.X, padx=50)
    
    def show_syllable_choice_exercise(self, exercise):
        sentence_parts = exercise["sentence"].split("___")
        sentence_text = f"Complete the sentence: {sentence_parts[0]}____{sentence_parts[1] if len(sentence_parts) > 1 else ''}"
        
        question_label = self.create_label(self.content_frame, sentence_text, style="body")
        question_label.pack(pady=(0, 10))
        
        hint_label = self.create_label(self.content_frame, f"Hint: {exercise['hint']}", style="hint")
        hint_label.pack(pady=(0, 20))
        
        for i, option in enumerate(exercise["syllable_options"]):
            btn = self.create_button(self.content_frame, option,
                                   lambda idx=i: self.check_syllable_choice(exercise, idx),
                                   style="korean")
            btn.pack(pady=5, fill=tk.X, padx=50)
    
    def show_word_building_exercise(self, exercise):
        question_label = self.create_label(self.content_frame, exercise["question"], style="body")
        question_label.pack(pady=(0, 20))
        
        # Show current word being built
        self.built_word = ""
        self.word_display = self.create_label(self.content_frame, "[ ]", 
                                            font=('Arial', 24, 'bold'), fg='#dc2626')
        self.word_display.pack(pady=(0, 20))
        
        # Syllable buttons
        self.create_syllable_grid(exercise)
        
        # Control buttons
        self.create_word_building_controls(exercise)
    
    def create_syllable_grid(self, exercise):
        """Create grid of syllable buttons for word building"""
        syllable_frame = self.create_content_frame(self.content_frame)
        syllable_frame.pack(pady=10)
        
        for i, syllable in enumerate(exercise["syllable_parts"]):
            btn = self.create_button(syllable_frame, syllable,
                                   lambda s=syllable: self.add_syllable(s, exercise),
                                   font=('Arial', 16, 'bold'), bg='#f9fafb', fg='#1f2937',
                                   padx=15, pady=8, relief=tk.SOLID, bd=1)
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    
    def create_word_building_controls(self, exercise):
        """Create clear and submit buttons for word building"""
        button_frame = self.create_content_frame(self.content_frame)
        button_frame.pack(pady=20)
        
        clear_btn = self.create_button(button_frame, "Clear", self.clear_built_word, style="danger")
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        submit_btn = self.create_button(button_frame, "Submit", 
                                      lambda: self.check_word_building(exercise), style="action")
        submit_btn.pack(side=tk.LEFT, padx=10)
    
    def add_syllable(self, syllable, exercise):
        self.built_word += syllable
        self.word_display.config(text=f"[ {self.built_word} ]")
    
    def clear_built_word(self):
        self.built_word = ""
        self.word_display.config(text="[ ]")
    
    def check_multiple_choice(self, exercise, selected_idx):
        if selected_idx == exercise["correct"]:
            result_text = "Correct! " + exercise["explanation"]
            bg_color = '#d1fae5'
        else:
            result_text = f"Incorrect. The correct answer is: {exercise['options'][exercise['correct']]}. " + exercise["explanation"]
            bg_color = '#fecaca'
        
        self.show_result(result_text, bg_color)
    
    def check_syllable_choice(self, exercise, selected_idx):
        if selected_idx == exercise["correct"]:
            result_text = "Correct!"
            bg_color = '#d1fae5'
        else:
            result_text = f"Incorrect. The correct answer is: {exercise['syllable_options'][exercise['correct']]}"
            bg_color = '#fecaca'
        
        self.show_result(result_text, bg_color)
    
    def check_word_building(self, exercise):
        if self.built_word == exercise["target"]:
            result_text = "Correct! Perfect!"
            bg_color = '#d1fae5'
        else:
            result_text = f"Incorrect. The correct answer is: {exercise['target']}"
            bg_color = '#fecaca'
        
        self.show_result(result_text, bg_color)
    
    def show_result(self, result_text, bg_color):
        self.clear_content()
        
        result_frame = self.create_content_frame(self.content_frame, bg=bg_color, relief=tk.SOLID, bd=1)
        result_frame.pack(pady=50, padx=50, fill=tk.BOTH)
        
        result_label = self.create_label(result_frame, result_text, 
                                       style="body", bg=bg_color, wraplength=600)
        result_label.pack(pady=30, padx=30)
        
        next_btn = self.create_button(result_frame, "Next Exercise", self.next_exercise)
        next_btn.pack(pady=20)
    
    def next_exercise(self):
        self.current_exercise_index += 1
        self.show_exercises()
    
    def restart_exercises(self):
        self.current_exercise_index = 0
        self.show_exercises()

if __name__ == "__main__":
    root = tk.Tk()
    app = KoreanLearningApp(root)
    root.mainloop()