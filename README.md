# Korean Learning App

A desktop application for learning Korean with lesson management, progress tracking, and interactive exercises.

## Setup Instructions

### 1. Create the folder structure:
```
korean_learning_app/
├── korean_learning_app.py
├── lesson_manager.py
├── progress.json
└── lessons/
    └── lesson_01.json
```

### 2. File descriptions:

- **korean_learning_app.py** - Main application file
- **lesson_manager.py** - Handles lesson loading and progress tracking
- **progress.json** - Stores user progress (auto-created)
- **lessons/** - Folder containing lesson files

### 3. Running the app:

```bash
python korean_learning_app.py
```

### 4. Features:

**Lesson Selection Interface:**
- Shows all available lessons
- Displays completion status with checkmarks
- Shows overall progress percentage
- Allows jumping to any lesson

**Progress Tracking:**
- Automatically saves which lessons you've completed
- Tracks your current lesson
- Shows completion percentage
- Suggests next lesson to study

**Lesson Navigation:**
- Back button to return to lesson selection
- Clean separation between lesson selection and lesson content
- Consistent navigation within lessons

**Exercise Completion:**
- When you finish all exercises in a lesson, it's marked as completed
- Option to go directly to next lesson
- Option to restart exercises or return to lesson selection

### 5. Adding more lessons:

Create new lesson files in the `lessons/` folder:
- `lesson_02.json`
- `lesson_03.json`
- etc.

Each lesson file should follow the same format as `lesson_01.json` with `lesson_number` and `lesson_title` fields.

### 6. Progress file format:

The `progress.json` file automatically tracks:
- `last_completed_lesson` - Highest lesson number completed
- `completed_lessons` - Array of all completed lesson numbers
- `current_lesson` - Currently selected lesson
- `total_lessons_available` - Total lessons found in folder

### 7. Key improvements made:

**Code Organization:**
- Separated lesson data into external JSON files
- Created reusable UI component functions
- Broke down large methods into focused functions
- Added progress tracking system

**User Experience:**
- Lesson selection interface with visual progress
- Completion status indicators
- Smooth navigation between lessons
- Progress persistence between sessions

**Maintainability:**
- Centralized styling in component functions
- Modular lesson management
- Error handling for missing files
- Extensible lesson system