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
    
    def create_button(self, parent, text, command, 
                     font=('Arial', 14, 'bold'), 
                     bg='#ffffff', fg='#000000',
                     activebackground='#f3f4f6', activeforeground='#000000',
                     padx=15, pady=8, 
                     relief=tk.FLAT, bd=1, borderwidth=1,
                     **kwargs):
        """Create a button with customizable parameters"""
        return tk.Button(parent, text=text, command=command,
                        font=font, bg=bg, fg=fg,
                        activebackground=activebackground, activeforeground=activeforeground,
                        highlightbackground=bg,
                        padx=padx, pady=pady,
                        relief=relief, bd=bd, borderwidth=borderwidth,
                        **kwargs)
    
    def create_label(self, parent, text,
                    font=('Arial', 16), 
                    bg='#ffffff', fg='#374151',
                    justify=tk.LEFT,
                    **kwargs):
        """Create a label with customizable parameters"""
        return tk.Label(parent, text=text,
                       font=font, bg=bg, fg=fg,
                       justify=justify,
                       **kwargs)
    
    def create_content_frame(self, parent, bg='#ffffff', **kwargs):
        """Create a frame with customizable parameters"""
        return tk.Frame(parent, bg=bg, **kwargs)
    
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
        
        for text, command in nav_buttons:
            btn = self.create_button(self.nav_frame, text, command)
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
        title = self.create_label(self.top_frame, "Korean Learning App - Select Lesson", 
                                 font=('Arial', 24, 'bold'), fg='#1f2937')
        title.pack(pady=(0, 20))
        
        # Progress summary
        progress = self.lesson_manager.get_progress_summary()
        progress_text = f"Progress: {progress['completed_lessons']}/{progress['total_lessons']} lessons completed ({progress['completion_percentage']:.0f}%)"
        
        progress_label = self.create_label(self.top_frame, progress_text, 
                                          font=('Arial', 14), fg='#059669')
        progress_label.pack(pady=(0, 10))
        
        # Vocabulary review button
        vocab_review_btn = self.create_button(self.top_frame, "📚 Review All Vocabulary", 
                                            self.show_vocabulary_review, 
                                            bg='#059669', fg='white', relief=tk.RAISED, bd=2)
        vocab_review_btn.pack(pady=(0, 20))
        
        # Lesson list
        lessons = self.lesson_manager.get_available_lessons()
        
        if not lessons:
            no_lessons = self.create_label(self.content_frame, 
                                         "No lessons found. Please add lesson files to the 'lessons' folder.")
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
        lesson_frame = self.create_content_frame(parent, bg='#f9fafb', relief=tk.SOLID, bd=1)
        lesson_frame.pack(fill=tk.X, pady=5, padx=10)
        
        is_completed = self.lesson_manager.is_lesson_completed(lesson["number"])
        
        # Lesson info
        lesson_title = f"Lesson {lesson['number']}: {lesson['title']}"
        status = " ✓" if is_completed else ""
        
        # Different colors for completed vs incomplete lessons
        if is_completed:
            bg_color = '#d1fae5'
            fg_color = '#065f46'
            active_bg = '#a7f3d0'
        else:
            bg_color = '#f9fafb'
            fg_color = '#1f2937'
            active_bg = '#e5e7eb'
        
        lesson_btn = self.create_button(lesson_frame, lesson_title + status,
                                      lambda l=lesson: self.select_lesson(l["number"]),
                                      font=('Arial', 16, 'bold'),
                                      bg=bg_color, fg=fg_color,
                                      activebackground=active_bg, activeforeground=fg_color,
                                      padx=20, pady=15, relief=tk.SOLID, bd=1)
        lesson_btn.pack(fill=tk.X, padx=10, pady=10)
    
    def select_lesson(self, lesson_number):
        """Select and load a specific lesson"""
        self.current_lesson = self.lesson_manager.load_lesson(lesson_number)
        
        if not self.current_lesson:
            # Show error message
            self.clear_content()
            error_label = self.create_label(self.content_frame, 
                                          f"Error loading lesson {lesson_number}. Please check the lesson file.")
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
        title = self.create_label(self.top_frame, lesson_info, font=('Arial', 24, 'bold'), fg='#1f2937')
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
        
        overview_label = self.create_label(self.content_frame, overview_text)
        overview_label.pack(anchor=tk.W, pady=30)
    
    def show_vocabulary(self):
        self.clear_content()
        
        title = self.create_label(self.content_frame, "Vocabulary", font=('Arial', 20, 'bold'), fg='#1f2937')
        title.pack(pady=(0, 20), anchor=tk.W)
        
        # Calculate pagination
        vocab_list = self.current_lesson["vocabulary"]
        if not vocab_list:
            no_vocab = self.create_label(self.content_frame, "No vocabulary items in this lesson.")
            no_vocab.pack(pady=20)
            return
            
        total_pages = (len(vocab_list) + self.vocab_per_page - 1) // self.vocab_per_page
        start_idx = self.current_vocab_page * self.vocab_per_page
        end_idx = min(start_idx + self.vocab_per_page, len(vocab_list))
        
        # Show page info
        page_info = self.create_label(self.content_frame, 
                                    f"Page {self.current_vocab_page + 1} of {total_pages}", 
                                    font=('Arial', 14, 'italic'), fg='#6b7280')
        page_info.pack(pady=(0, 15), anchor=tk.W)
        
        # Show vocabulary for current page
        for vocab in vocab_list[start_idx:end_idx]:
            vocab_frame = self.create_content_frame(self.content_frame, bg='#f9fafb', relief=tk.SOLID, bd=1)
            vocab_frame.pack(fill=tk.X, pady=10, padx=0)
            
            korean_label = self.create_label(vocab_frame, vocab["korean"], 
                                           font=('Arial', 20, 'bold'), fg='#dc2626', bg='#f9fafb')
            korean_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
            
            rom_label = self.create_label(vocab_frame, f"[{vocab['romanization']}]", 
                                        font=('Arial', 14, 'italic'), fg='#6b7280', bg='#f9fafb')
            rom_label.pack(anchor=tk.W, padx=15)
            
            eng_label = self.create_label(vocab_frame, vocab["english"], 
                                        font=('Arial', 16), fg='#1f2937', bg='#f9fafb')
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
        
        title = self.create_label(self.content_frame, "Grammar", font=('Arial', 20, 'bold'), fg='#1f2937')
        title.pack(pady=(0, 20), anchor=tk.W)
        
        if not self.current_lesson["grammar_rules"]:
            no_grammar = self.create_label(self.content_frame, "No grammar rules in this lesson.")
            no_grammar.pack(pady=20)
            return
        
        for rule in self.current_lesson["grammar_rules"]:
            self.create_grammar_rule_display(rule)
        
        # Show example sentences
        if self.current_lesson["example_sentences"]:
            self.create_example_sentences_display()
    
    def create_grammar_rule_display(self, rule):
        """Create display for a single grammar rule"""
        rule_frame = self.create_content_frame(self.content_frame, bg='#f9fafb', relief=tk.SOLID, bd=1)
        rule_frame.pack(fill=tk.X, pady=10, padx=0)
        
        rule_title = self.create_label(rule_frame, rule["title"], 
                                     font=('Arial', 18, 'bold'), fg='#1f2937', bg='#f9fafb')
        rule_title.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        explanation = self.create_label(rule_frame, rule["explanation"], 
                                      bg='#f9fafb', wraplength=800)
        explanation.pack(anchor=tk.W, padx=15, pady=5)
        
        pattern = self.create_label(rule_frame, f"Pattern: {rule['pattern']}", 
                                  font=('Arial', 14, 'italic'), fg='#6b7280', bg='#f9fafb')
        pattern.pack(anchor=tk.W, padx=15, pady=5)
        
        if "formality_note" in rule:
            note = self.create_label(rule_frame, f"Note: {rule['formality_note']}", 
                                   font=('Arial', 12), bg='#f9fafb', fg='#6b7280')
            note.pack(anchor=tk.W, padx=15, pady=(0, 10))
    
    def create_example_sentences_display(self):
        """Create display for example sentences"""
        examples_title = self.create_label(self.content_frame, "Example Sentences", 
                                         font=('Arial', 18, 'bold'), fg='#1f2937')
        examples_title.pack(pady=(30, 15), anchor=tk.W)
        
        for example in self.current_lesson["example_sentences"]:
            example_frame = self.create_content_frame(self.content_frame, bg='#f9fafb', relief=tk.SOLID, bd=1)
            example_frame.pack(fill=tk.X, pady=5, padx=0)
            
            korean_label = self.create_label(example_frame, example["korean"], 
                                           font=('Arial', 20, 'bold'), fg='#dc2626', bg='#f9fafb')
            korean_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
            
            rom_label = self.create_label(example_frame, example["romanization"], 
                                        font=('Arial', 14, 'italic'), fg='#6b7280', bg='#f9fafb')
            rom_label.pack(anchor=tk.W, padx=15)
            
            eng_label = self.create_label(example_frame, example["english"], 
                                        font=('Arial', 16), fg='#1f2937', bg='#f9fafb')
            eng_label.pack(anchor=tk.W, padx=15, pady=(0, 10))
    
    def show_exercises(self):
        self.clear_content()
        
        if not self.current_lesson["exercises"]:
            no_exercises = self.create_label(self.content_frame, "No exercises in this lesson.")
            no_exercises.pack(pady=50)
            return
        
        if self.current_exercise_index >= len(self.current_lesson["exercises"]):
            self.show_exercises_completed()
            return
        
        exercise = self.current_lesson["exercises"][self.current_exercise_index]
        
        title = self.create_label(self.content_frame, 
                                f"Exercise {self.current_exercise_index + 1} of {len(self.current_lesson['exercises'])}", 
                                font=('Arial', 20, 'bold'), fg='#1f2937')
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
                                       self.restart_exercises, 
                                       bg='#059669', fg='white', relief=tk.RAISED, bd=2)
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        lessons_btn = self.create_button(button_frame, "Back to Lessons", 
                                       self.show_lesson_selection)
        lessons_btn.pack(side=tk.LEFT, padx=10)
        
        # Show next lesson button if available
        next_lesson_num = self.lesson_manager.get_next_lesson()
        if self.lesson_manager.get_lesson_info(next_lesson_num):
            next_btn = self.create_button(button_frame, f"Next Lesson ({next_lesson_num})", 
                                        lambda: self.select_lesson(next_lesson_num), 
                                        bg='#059669', fg='white', relief=tk.RAISED, bd=2)
            next_btn.pack(side=tk.LEFT, padx=10)
    
    def show_multiple_choice_exercise(self, exercise):
        question_label = self.create_label(self.content_frame, exercise["question"])
        question_label.pack(pady=(0, 20))
        
        for i, option in enumerate(exercise["options"]):
            btn = self.create_button(self.content_frame, option,
                                   lambda idx=i: self.check_multiple_choice(exercise, idx),
                                   font=('Arial', 16), bg='#f9fafb', fg='#1f2937',
                                   padx=20, pady=10, relief=tk.SOLID, bd=1)
            btn.pack(pady=5, fill=tk.X, padx=50)
    
    def show_syllable_choice_exercise(self, exercise):
        sentence_parts = exercise["sentence"].split("___")
        sentence_text = f"Complete the sentence: {sentence_parts[0]}____{sentence_parts[1] if len(sentence_parts) > 1 else ''}"
        
        question_label = self.create_label(self.content_frame, sentence_text)
        question_label.pack(pady=(0, 10))
        
        hint_label = self.create_label(self.content_frame, f"Hint: {exercise['hint']}", 
                                     font=('Arial', 14, 'italic'), fg='#6b7280')
        hint_label.pack(pady=(0, 20))
        
        for i, option in enumerate(exercise["syllable_options"]):
            btn = self.create_button(self.content_frame, option,
                                   lambda idx=i: self.check_syllable_choice(exercise, idx),
                                   font=('Arial', 18, 'bold'), bg='#f9fafb', fg='#dc2626',
                                   padx=20, pady=10, relief=tk.SOLID, bd=1)
            btn.pack(pady=5, fill=tk.X, padx=50)
    
    def show_word_building_exercise(self, exercise):
        question_label = self.create_label(self.content_frame, exercise["question"])
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
        
        clear_btn = self.create_button(button_frame, "Clear", self.clear_built_word, 
                                     bg='#dc2626', fg='white', relief=tk.RAISED, bd=2)
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        submit_btn = self.create_button(button_frame, "Submit", 
                                      lambda: self.check_word_building(exercise), 
                                      bg='#059669', fg='white', relief=tk.RAISED, bd=2)
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
                                       bg=bg_color, wraplength=600)
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
    
    def show_vocabulary_review(self):
        """Show vocabulary review for all completed lessons plus current lesson"""
        self.clear_content()
        
        # Clear top frame and show review title
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        
        title = self.create_label(self.top_frame, "📚 Vocabulary Review", font=('Arial', 24, 'bold'), fg='#1f2937')
        title.pack(pady=(0, 10))
        
        # Back button
        back_btn = self.create_button(self.top_frame, "← Back to Lessons", 
                                    self.show_lesson_selection)
        back_btn.pack(pady=(0, 20))
        
        # Get vocabulary from completed lessons + current lesson
        vocab_by_lesson = self.get_learned_vocabulary()
        
        if not vocab_by_lesson:
            no_vocab = self.create_label(self.content_frame, 
                                       "No vocabulary learned yet. Complete some lessons to see your vocabulary here!")
            no_vocab.pack(pady=50)
            return
        
        # Create vocabulary display options
        self.vocab_review_mode = "by_lesson"  # or "all_words"
        self.create_vocabulary_review_controls()
        self.display_vocabulary_review(vocab_by_lesson)
    
    def create_vocabulary_review_controls(self):
        """Create controls for vocabulary review display"""
        controls_frame = self.create_content_frame(self.content_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        mode_label = self.create_label(controls_frame, "View Mode:")
        mode_label.pack(side=tk.LEFT, padx=(0, 10))
        
        by_lesson_btn = self.create_button(controls_frame, "By Lesson", 
                                         lambda: self.switch_vocab_mode("by_lesson"))
        by_lesson_btn.pack(side=tk.LEFT, padx=5)
        
        all_words_btn = self.create_button(controls_frame, "All Words", 
                                         lambda: self.switch_vocab_mode("all_words"))
        all_words_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats
        vocab_by_lesson = self.get_learned_vocabulary()
        total_words = sum(len(words) for words in vocab_by_lesson.values())
        total_lessons = len(vocab_by_lesson)
        
        stats_text = f"Total: {total_words} words from {total_lessons} lessons"
        stats_label = self.create_label(controls_frame, stats_text, 
                                      font=('Arial', 14, 'italic'), fg='#6b7280')
        stats_label.pack(side=tk.RIGHT)
    
    def switch_vocab_mode(self, mode):
        """Switch between vocabulary review modes"""
        self.vocab_review_mode = mode
        vocab_by_lesson = self.get_learned_vocabulary()
        
        # Clear existing display
        for widget in self.content_frame.winfo_children():
            if widget.winfo_class() != "Frame":  # Keep controls frame
                widget.destroy()
            elif hasattr(widget, 'vocab_display'):  # Remove vocab display frames
                widget.destroy()
        
        self.display_vocabulary_review(vocab_by_lesson)
    
    def get_learned_vocabulary(self):
        """Get vocabulary from completed lessons plus current lesson"""
        vocab_by_lesson = {}
        
        # Get completed lessons
        completed_lessons = self.lesson_manager.progress_data["completed_lessons"]
        current_lesson_num = self.lesson_manager.get_current_lesson()
        
        # Include current lesson in review
        lessons_to_include = set(completed_lessons + [current_lesson_num])
        
        for lesson_num in sorted(lessons_to_include):
            lesson_data = self.lesson_manager.load_lesson(lesson_num)
            if lesson_data and lesson_data.get("vocabulary"):
                lesson_title = f"Lesson {lesson_num}: {lesson_data.get('lesson_title', 'Unknown')}"
                vocab_by_lesson[lesson_title] = lesson_data["vocabulary"]
        
        return vocab_by_lesson
    
    def display_vocabulary_review(self, vocab_by_lesson):
        """Display vocabulary review based on current mode"""
        # Create scrollable frame for vocabulary
        canvas = tk.Canvas(self.content_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = self.create_content_frame(canvas)
        scrollable_frame.vocab_display = True  # Mark as vocab display frame
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        if self.vocab_review_mode == "by_lesson":
            self.display_vocab_by_lesson(scrollable_frame, vocab_by_lesson)
        else:
            self.display_all_vocab_words(scrollable_frame, vocab_by_lesson)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def display_vocab_by_lesson(self, parent, vocab_by_lesson):
        """Display vocabulary organized by lesson"""
        for lesson_title, vocabulary in vocab_by_lesson.items():
            # Lesson header
            lesson_header = self.create_label(parent, lesson_title, 
                                            font=('Arial', 18, 'bold'), fg='#1f2937')
            lesson_header.pack(anchor=tk.W, pady=(20, 10))
            
            # Vocabulary cards for this lesson
            for vocab in vocabulary:
                vocab_frame = self.create_content_frame(parent, bg='#f9fafb', relief=tk.SOLID, bd=1)
                vocab_frame.pack(fill=tk.X, pady=5, padx=10)
                
                # Horizontal layout for compact display
                content_frame = self.create_content_frame(vocab_frame)
                content_frame.pack(fill=tk.X, padx=15, pady=10)
                
                korean_label = self.create_label(content_frame, vocab["korean"], 
                                               font=('Arial', 18, 'bold'), fg='#dc2626', bg='#f9fafb')
                korean_label.pack(side=tk.LEFT)
                
                rom_label = self.create_label(content_frame, f"[{vocab['romanization']}]", 
                                            font=('Arial', 14, 'italic'), fg='#6b7280', bg='#f9fafb')
                rom_label.pack(side=tk.LEFT, padx=(10, 0))
                
                eng_label = self.create_label(content_frame, f"- {vocab['english']}", 
                                            font=('Arial', 16), fg='#1f2937', bg='#f9fafb')
                eng_label.pack(side=tk.LEFT, padx=(10, 0))
    
    def display_all_vocab_words(self, parent, vocab_by_lesson):
        """Display all vocabulary words in alphabetical order"""
        # Flatten all vocabulary
        all_vocab = []
        for lesson_title, vocabulary in vocab_by_lesson.items():
            for vocab in vocabulary:
                vocab_with_lesson = vocab.copy()
                vocab_with_lesson["lesson"] = lesson_title
                all_vocab.append(vocab_with_lesson)
        
        # Sort by Korean word
        all_vocab.sort(key=lambda x: x["korean"])
        
        # Display header
        header = self.create_label(parent, f"All Vocabulary ({len(all_vocab)} words)", 
                                 font=('Arial', 18, 'bold'), fg='#1f2937')
        header.pack(anchor=tk.W, pady=(10, 20))
        
        # Display vocabulary
        for vocab in all_vocab:
            vocab_frame = self.create_content_frame(parent, bg='#f9fafb', relief=tk.SOLID, bd=1)
            vocab_frame.pack(fill=tk.X, pady=3, padx=10)
            
            # Main content
            content_frame = self.create_content_frame(vocab_frame)
            content_frame.pack(fill=tk.X, padx=15, pady=8)
            
            # Korean and pronunciation
            top_line = self.create_content_frame(content_frame)
            top_line.pack(fill=tk.X)
            
            korean_label = self.create_label(top_line, vocab["korean"], 
                                           font=('Arial', 18, 'bold'), fg='#dc2626', bg='#f9fafb')
            korean_label.pack(side=tk.LEFT)
            
            rom_label = self.create_label(top_line, f"[{vocab['romanization']}]", 
                                        font=('Arial', 14, 'italic'), fg='#6b7280', bg='#f9fafb')
            rom_label.pack(side=tk.LEFT, padx=(10, 0))
            
            # English and lesson info
            bottom_line = self.create_content_frame(content_frame)
            bottom_line.pack(fill=tk.X)
            
            eng_label = self.create_label(bottom_line, vocab["english"], 
                                        font=('Arial', 16), fg='#1f2937', bg='#f9fafb')
            eng_label.pack(side=tk.LEFT)
            
            lesson_label = self.create_label(bottom_line, f"({vocab['lesson']})", 
                                           font=('Arial', 12), fg='#6b7280', bg='#f9fafb')
            lesson_label.pack(side=tk.RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    app = KoreanLearningApp(root)
    root.mainloop()