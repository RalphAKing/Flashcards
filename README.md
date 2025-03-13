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

## License

This project is open-source and available for modification and use under the MIT license.

### MIT License

```
MIT License

Copyright (c) 2025 Ralph King

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
