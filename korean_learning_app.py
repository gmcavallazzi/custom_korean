import tkinter as tk
from tkinter import ttk
import json
import os
from pathlib import Path
from lesson_manager import LessonManager

class KoreanLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Learning App")
        self.root.geometry("1200x800")
        self.root.configure(bg='#ffffff')
        
        # Initialize lesson manager
        self.lesson_manager = LessonManager()
        
        # Load current lesson
        current_lesson_num = self.lesson_manager.get_current_lesson()
        self.current_lesson = self.lesson_manager.load_lesson(current_lesson_num)
        
        # Exercise state
        self.current_exercise_index = 0
        self.current_vocab_page = 0
        self.vocab_per_page = 3
        self.exercises_completed_count = 0
        
        # Create UI
        self.create_widgets()
        self.show_lesson_selection()
    
    def create_button(self, parent, text, command, style="default", **kwargs):
        """Create standardized buttons with consistent styling"""
        styles = {
            "default": {
                "font": ('Arial', 14, 'bold'),
                "bg": '#ffffff',
                "fg": '#000000',
                "activebackground": '#f3f4f6',
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
                "activebackground": '#f3f4f6',
                "activeforeground": '#000000',
                "highlightbackground": '#ffffff',
                "padx": 15,
                "pady": 8,
                "relief": tk.FLAT,
                "bd": 1,
                "borderwidth": 1
            },
            "lesson_select": {
                "font": ('Arial', 16, 'bold'),
                "bg": '#f9fafb',
                "fg": '#1f2937',
                "activebackground": '#e5e7eb',
                "activeforeground": '#1f2937',
                "padx": 20,
                "pady": 15,
                "relief": tk.SOLID,
                "bd": 1
            },
            "lesson_completed": {
                "font": ('Arial', 16, 'bold'),
                "bg": '#d1fae5',
                "fg": '#065f46',
                "activebackground": '#a7f3d0',
                "activeforeground": '#065f46',
                "padx": 20,
                "pady": 15,
                "relief": tk.SOLID,
                "bd": 1
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
            },
            "back": {
                "font": ('Arial', 14, 'bold'),
                "bg": '#ffffff',
                "fg": '#000000',
                "activebackground": '#f3f4f6',
                "activeforeground": '#000000',
                "highlightbackground": '#ffffff',
                "padx": 15,
                "pady": 8,
                "relief": tk.FLAT,
                "bd": 1,
                "borderwidth": 1
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
            },
            "progress": {
                "font": ('Arial', 14),
                "bg": '#ffffff',
                "fg": '#059669'
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
        
        # Top section for lesson selection and progress
        self.top_frame = self.create_content_frame(main_frame)
        self.top_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Navigation buttons (initially hidden)
        self.nav_frame = self.create_content_frame(main_frame)
        self.nav_frame.pack(fill=tk.X, pady=(0, 20))
        self.nav_frame.pack_forget()  # Hide initially
        
        # Content frame
        self.content_frame = self.create_content_frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_lesson_navigation(self):
        """Show lesson navigation buttons"""
        # Clear existing nav buttons
        for widget in self.nav_frame.winfo_children():
            widget.destroy()
        
        nav_buttons = [
            ("← Back to Lessons", self.show_lesson_selection),
            ("Lesson Overview", self.show_lesson_overview),
            ("Vocabulary", self.show_vocabulary),
            ("Grammar", self.show_grammar),
            ("Exercises", self.show_exercises)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            style = "back" if i == 0 else "nav"
            btn = self.create_button(self.nav_frame, text, command, style=style)
            btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.nav_frame.pack(fill=tk.X, pady=(0, 20))
    
    def hide_lesson_navigation(self):
        """Hide lesson navigation buttons"""
        self.nav_frame.pack_forget()
    
    def clear_content(self):
        """Clear all widgets from content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_lesson_selection(self):
        """Show lesson selection interface"""
        self.hide_lesson_navigation()
        self.clear_content()
        
        # Clear top frame
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        
        # Title
        title = self.create_label(self.top_frame, "Korean Learning App - Select Lesson", style="title")
        title.pack(pady=(0, 20))
        
        # Progress summary
        progress = self.lesson_manager.get_progress_summary()
        progress_text = f"Progress: {progress['completed_lessons']}/{progress['total_lessons']} lessons completed ({progress['completion_percentage']:.0f}%)"
        
        progress_label = self.create_label(self.top_frame, progress_text, style="progress")
        progress_label.pack(pady=(0, 20))
        
        # Lesson list
        lessons = self.lesson_manager.get_available_lessons()
        
        if not lessons:
            no_lessons = self.create_label(self.content_frame, 
                                         "No lessons found. Please add lesson files to the 'lessons' folder.", 
                                         style="body")
            no_lessons.pack(pady=50)
            return
        
        # Create scrollable frame for lessons
        canvas = tk.Canvas(self.content_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = self.create_content_frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add lessons to scrollable frame
        for lesson in lessons:
            self.create_lesson_button(scrollable_frame, lesson)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_lesson_button(self, parent, lesson):
        """Create a button for lesson selection"""
        lesson_frame = self.create_content_frame(parent, style="card")
        lesson_frame.pack(fill=tk.X, pady=5, padx=10)
        
        is_completed = self.lesson_manager.is_lesson_completed(lesson["number"])
        
        # Lesson info
        lesson_title = f"Lesson {lesson['number']}: {lesson['title']}"
        status = " ✓" if is_completed else ""
        
        button_style = "lesson_completed" if is_completed else "lesson_select"
        
        lesson_btn = self.create_button(lesson_frame, lesson_title + status,
                                      lambda l=lesson: self.select_lesson(l["number"]),
                                      style=button_style)
        lesson_btn.pack(fill=tk.X, padx=10, pady=10)
    
    def select_lesson(self, lesson_number):
        """Select and load a specific lesson"""
        self.current_lesson = self.lesson_manager.load_lesson(lesson_number)
        
        if not self.current_lesson:
            # Show error message
            self.clear_content()
            error_label = self.create_label(self.content_frame, 
                                          f"Error loading lesson {lesson_number}. Please check the lesson file.", 
                                          style="body")
            error_label.pack(pady=50)
            return
        
        # Update current lesson in progress
        self.lesson_manager.set_current_lesson(lesson_number)
        
        # Reset exercise state
        self.current_exercise_index = 0
        self.current_vocab_page = 0
        self.exercises_completed_count = 0
        
        # Show lesson navigation and overview
        self.show_lesson_navigation()
        self.show_lesson_overview()
    
    def show_lesson_overview(self):
        self.clear_content()
        
        # Clear top frame and show lesson info
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        
        lesson_info = f"Lesson {self.current_lesson['lesson_number']}: {self.current_lesson['lesson_title']}"
        title = self.create_label(self.top_frame, lesson_info, style="title")
        title.pack(pady=(0, 10))
        
        # Show completion status
        is_completed = self.lesson_manager.is_lesson_completed(self.current_lesson['lesson_number'])
        status_text = "✓ Completed" if is_completed else "In Progress"
        status_color = "#059669" if is_completed else "#6b7280"
        
        status_label = self.create_label(self.top_frame, status_text, 
                                       font=('Arial', 14, 'bold'), fg=status_color)
        status_label.pack()
        
        overview_text = f"""
{len(self.current_lesson['vocabulary'])} vocabulary words
{len(self.current_lesson['grammar_rules'])} grammar rules  
{len(self.current_lesson['exercises'])} exercises

Use the navigation buttons above to explore different sections of this lesson."""
        
        overview_label = self.create_label(self.content_frame, overview_text, style="body")
        overview_label.pack(anchor=tk.W, pady=30)
    
    def show_vocabulary(self):
        self.clear_content()
        
        title = self.create_label(self.content_frame, "Vocabulary", style="subtitle")
        title.pack(pady=(0, 20), anchor=tk.W)
        
        # Calculate pagination
        vocab_list = self.current_lesson["vocabulary"]
        if not vocab_list:
            no_vocab = self.create_label(self.content_frame, "No vocabulary items in this lesson.", style="body")
            no_vocab.pack(pady=20)
            return
            
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
        
        if not self.current_lesson["grammar_rules"]:
            no_grammar = self.create_label(self.content_frame, "No grammar rules in this lesson.", style="body")
            no_grammar.pack(pady=20)
            return
        
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
        
        if not self.current_lesson["exercises"]:
            no_exercises = self.create_label(self.content_frame, "No exercises in this lesson.", style="body")
            no_exercises.pack(pady=50)
            return
        
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
        """Display completion message and options"""
        completed_label = self.create_label(self.content_frame, "All exercises completed! Great job!", 
                                          font=('Arial', 20, 'bold'), fg='#059669')
        completed_label.pack(pady=50)
        
        # Mark lesson as completed
        self.lesson_manager.mark_lesson_completed(self.current_lesson['lesson_number'])
        
        button_frame = self.create_content_frame(self.content_frame)
        button_frame.pack(pady=20)
        
        restart_btn = self.create_button(button_frame, "Restart Exercises", 
                                       self.restart_exercises, style="action")
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        lessons_btn = self.create_button(button_frame, "Back to Lessons", 
                                       self.show_lesson_selection, style="back")
        lessons_btn.pack(side=tk.LEFT, padx=10)
        
        # Show next lesson button if available
        next_lesson_num = self.lesson_manager.get_next_lesson()
        if self.lesson_manager.get_lesson_info(next_lesson_num):
            next_btn = self.create_button(button_frame, f"Next Lesson ({next_lesson_num})", 
                                        lambda: self.select_lesson(next_lesson_num), style="action")
            next_btn.pack(side=tk.LEFT, padx=10)
    
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
        self.exercises_completed_count += 1
        self.show_exercises()
    
    def restart_exercises(self):
        self.current_exercise_index = 0
        self.exercises_completed_count = 0
        self.show_exercises()

if __name__ == "__main__":
    root = tk.Tk()
    app = KoreanLearningApp(root)
    root.mainloop()