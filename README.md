# RASA Chatbot - Educational Institution Assistant

A comprehensive RASA-based conversational AI chatbot designed to provide information about an educational institution (NIST). The bot answers queries about admissions, courses, fees, placements, campus facilities, and more.

## 🎯 Features

- **Multi-intent NLU**: Handles 30+ intents for various educational queries
- **Course Information**: Detailed information on B.Tech, M.Tech, and PhD programs
- **Admission Assistance**: Guidance on admission processes and requirements
- **Fee Information**: Course-wise fee details
- **Placement Data**: Placement statistics and opportunities
- **Campus Facilities**: Information about hostels, sports, library, cafeteria, etc.
- **Alumni Network**: Alumni information and success stories
- **Event Updates**: Information about workshops, FDP, and convocations
- **Web Integration**: Flask-based backend with PostgreSQL database
- **Web UI**: HTML/CSS/JavaScript frontend with floating chat widget
- **Authentication**: Login system with database verification

## 📋 Project Structure

```
RASA_BOT/
├── actions/
│   ├── __init__.py
│   └── actions.py              # Custom RASA actions
├── data/
│   ├── nlu.yml                 # Natural Language Understanding training data
│   ├── stories.yml             # Conversation flow stories
│   └── rules.yml               # Business rules
├── models/                      # Trained RASA models (generated)
├── tests/
│   └── test_stories.yml        # Test scenarios
├── LOGIN NIS/                  # Additional login interface
│   ├── dashboard.html
│   ├── loginnew.html
│   ├── loginnew.css
│   └── images/
├── images/                     # Project images
├── js/                         # JavaScript files
├── app.py                      # Flask backend server
├── chat.js                     # Chatbot widget logic
├── index.html                  # Main web interface
├── style.css                   # Styling
├── config.yml                  # RASA NLU/Core configuration
├── domain.yml                  # RASA domain definition
├── credentials.yml             # RASA channel credentials
├── endpoints.yml               # RASA endpoints configuration
├── courses_db.json             # Course database
├── wbauthusers.sql             # Database schema
├── rasa_dbsetup.py             # Database setup script
├── auto_train_pipeline.py      # Automatic training script
└── .gitignore                  # Git ignore rules
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/pbharatchandra/RASA_BOT.git
cd RASA_BOT
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\Activate          # Windows
source .venv/bin/activate       # Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install rasa rasa-sdk flask flask-cors psycopg2-binary python-dotenv gspread google-auth-oauthlib google-generativeai
```

### Step 4: Setup Database
```bash
# Configure database connection in app.py
python rasa_dbsetup.py
```

### Step 5: Train RASA Model
```bash
rasa train
```

## 🚀 Running the Chatbot

### Terminal 1 - RASA Backend (API)
```bash
rasa run --enable-api --cors "*"
```

### Terminal 2 - RASA Actions Server
```bash
rasa run actions
```

### Terminal 3 - Flask Server (Optional)
```bash
python app.py
```

## 📚 Supported Intents

The chatbot handles the following intents:

| Intent | Description |
|--------|-------------|
| `greet` | Greeting messages |
| `goodbye` | Farewell messages |
| `thankyou` | Gratitude expressions |
| `ask_admission` | General admission queries |
| `ask_course_details` | Course information |
| `ask_fees` | Fee structure |
| `ask_placements` | Placement statistics |
| `ask_contact` | Contact information |
| `ask_campus_facilities` | Hostel, library, sports, cafeteria info |
| `ask_about_hostels` | Hostel details |
| `ask_about_sports_facilities` | Sports facilities |
| `ask_research` | Research opportunities |
| `ask_achievements` | Institution achievements |
| `ask_events` | Upcoming events |
| `ask_alumni` | Alumni information |
| `ask_testimonials` | Student testimonials |
| `anti_ragging` | Anti-ragging policies |
| `counseling_service` | Counseling services |
| `fdp_info` | Faculty Development Programs |
| `workshops_info` | Workshop information |

## 🎓 Entity Recognition

The NLU pipeline recognizes:
- **course**: Course names (B.Tech, M.Tech, PhD)
- **entrance_exam**: Entrance examination names

## 💾 Database Configuration

The chatbot uses PostgreSQL with the following configuration (in `app.py`):

```python
DB_HOST = "localhost"
DB_NAME = "rasa_db"
DB_USER = "rasa_user"
DB_PASS = "rootadmin"
DB_PORT = "5432"
```

**Update these credentials** to match your PostgreSQL setup.

## 🌐 Web Integration

### Frontend Features
- **Floating Chat Widget**: Non-intrusive chat interface
- **Responsive Design**: Mobile and desktop compatible
- **Login System**: User authentication
- **Dashboard**: User dashboard interface

### Backend (Flask)
- `/login` - User authentication endpoint
- CORS enabled for cross-origin requests
- Database integration for user management

## ⚙️ Configuration Files

### `config.yml`
- NLU pipeline configuration
- Model architecture settings
- Language: English

### `domain.yml`
- Intents and entities definition
- Action definitions
- Response templates

### `credentials.yml`
- RASA channel configurations (rest, web, etc.)

### `endpoints.yml`
- Action server endpoint
- NLU server endpoint

## 📊 Training Data

### NLU Training (`data/nlu.yml`)
Contains 318+ lines of training examples across 30+ intents for robust intent classification.

### Stories (`data/stories.yml`)
Defines conversation flows and multi-turn dialogue patterns.

### Rules (`data/rules.yml`)
Specific business rules and deterministic responses.

## 🔐 Security

- User authentication via database
- Password hashing (implement if needed)
- CORS configuration for controlled access
- Environment variables for sensitive data (`.env`)

## 🚢 Deployment

For production deployment:
1. Use environment variables for sensitive data
2. Configure PostgreSQL for production
3. Set up proper logging
4. Implement SSL/TLS for security
5. Use a production WSGI server (Gunicorn, uWSGI)

## 🐛 Troubleshooting

### Issue: "Port 5005 already in use"
```bash
# Kill existing process or specify different port
rasa run --port 5006 --enable-api --cors "*"
```

### Issue: Database connection failed
- Verify PostgreSQL is running
- Check credentials in `app.py`
- Ensure database exists: `rasa_db`

### Issue: CORS errors
- The `--cors "*"` flag enables all origins
- Configure specific origins in production

## 📝 Useful Commands

| Command | Purpose |
|---------|---------|
| `rasa train` | Train the NLU and Core models |
| `rasa test` | Test stories and NLU |
| `rasa shell` | Interactive shell for testing |
| `rasa run actions` | Start action server on port 5055 |
| `rasa run --enable-api --cors "*"` | Start RASA server with API |
| `python auto_train_pipeline.py` | Automated training |

## 🤝 Contributing

1. Create a new branch for features
2. Make your changes
3. Test thoroughly
4. Push to GitHub
5. Create a Pull Request

## 📞 Support

For issues and questions:
- Check existing GitHub issues
- Create a new issue with detailed description
- Include error logs and system information

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

**P. Bharat Chandra**  
GitHub: [@pbharatchandra](https://github.com/pbharatchandra)

---

**Last Updated**: January 13, 2026
