# Flashcards Application

A web-based flashcards application built with Flask and MongoDB that allows users to create, manage, and study custom flashcard decks.

## Features

- User authentication and account management
- Create and manage multiple flashcard decks
- Import/Export decks via CSV files
- Interactive study mode
- Secure data handling with sanitized inputs
- Personal board creation for each user

## Technical Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Security**: Werkzeug password hashing
- **Data Sanitization**: Bleach
- **File Format**: CSV for deck storage

## Usage

1. Register/Login to your account
2. Navigate to the Decks section
3. Create a new deck or import existing CSV
4. Add flashcards with questions and answers
5. Study your decks in interactive mode
6. Download decks for backup or sharing

## API Endpoints

- `/login` - User authentication
- `/decks` - List all user decks
- `/deck/create` - Create new deck
- `/deck/edit/<deck_name>` - Edit deck contents
- `/deck/delete/<deck_name>` - Remove deck
- `/study/<deck_name>` - Study mode
- `/deck/download/<deck_name>` - Export deck as CSV

## Security Features

- Password hashing
- Input sanitization
- Session management
- User-specific file access
- MongoDB security best practices

