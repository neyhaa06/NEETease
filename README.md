# \# neetEase – AI-Powered NEET Preparation \& Student Well-being Platform

# 

# neetEase is an integrated web-based platform designed to support NEET aspirants through personalized study resources, mock tests, academic performance analytics, and student well-being monitoring.

# 

# The project combines Django, Data Science, and Machine Learning to provide a more personalized and data-driven learning experience.

# 

# \## Key Features

# 

# \- \*\*Student Dashboard:\*\* Centralized access to learning and well-being features.

# \- \*\*Study Materials:\*\* Subject-wise learning resources for Physics, Chemistry, and Biology.

# \- \*\*Mock Tests:\*\* Interactive tests with automated scoring and result tracking.

# \- \*\*Performance Analytics:\*\* Visual analysis of test scores, accuracy, and academic progress.

# \- \*\*Well-being Monitoring:\*\* Daily tracking of mood, stress, sleep, and study hours.

# \- \*\*AI-Based Stress Prediction:\*\* Machine Learning model that predicts stress categories using lifestyle patterns.

# \- \*\*Personalized Insights:\*\* Recommendations based on student performance and lifestyle information.

# \- \*\*Student Profile:\*\* Account management and profile information.

# 

# \## Machine Learning Implementation

# 

# The project uses a Logistic Regression classifier to predict student stress levels.

# 

# \*\*Dataset:\*\* Daily Lifestyle and Academic Performance of Students

# 

# \*\*Dataset characteristics:\*\*

# \- 2,000 student records

# \- Five lifestyle-based input features

# \- Target variable: Stress\_Level

# 

# \*\*Input features:\*\*

# \- Study Hours Per Day

# \- Extracurricular Hours Per Day

# \- Sleep Hours Per Day

# \- Social Hours Per Day

# \- Physical Activity Hours Per Day

# 

# \*\*Model:\*\* Logistic Regression

# 

# \*\*Preprocessing:\*\* SimpleImputer and StandardScaler

# 

# \*\*Evaluation:\*\*

# \- Train-test split: 80:20

# \- Random state: 42

# \- Model accuracy: 84.25%

# 

# The trained model is saved using Joblib and used for stress prediction.

# 

# \## Technology Stack

# 

# | Category | Technologies |

# |---|---|

# | Backend | Python, Django |

# | Frontend | HTML, CSS, JavaScript |

# | Database | SQLite |

# | Data Analysis | Pandas, NumPy |

# | Machine Learning | Scikit-learn |

# | Model Storage | Joblib |

# | Visualization | Chart.js, Matplotlib |

# | Development | Visual Studio Code |

# 

# \## Project Structure

# 

# ```text

# neetEase/

# │

# ├── config/

# │   ├── settings.py

# │   ├── urls.py

# │   ├── asgi.py

# │   └── wsgi.py

# │

# ├── core/

# │   ├── migrations/

# │   ├── templates/

# │   ├── data/

# │   ├── models.py

# │   ├── views.py

# │   └── admin.py

# │

# ├── ml/

# │   ├── artifacts/

# │   │   ├── stress\_classifier.joblib

# │   │   └── evaluation.json

# │   ├── train\_model.py

# │   └── test\_prediction.py

# │

# ├── manage.py

# ├── requirements.txt

# └── .gitignore

# ```

# 

# \## Installation and Setup

# 

# \### 1. Clone the repository

# 

# ```bash

# git clone https://github.com/neyhaa06/NEETease.git

# cd NEETease

# ```

# 

# \### 2. Create a virtual environment

# 

# ```bash

# python -m venv .venv

# ```

# 

# \### 3. Activate the environment

# 

# Windows PowerShell:

# 

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# ```

# 

# \### 4. Install dependencies

# 

# ```bash

# pip install -r requirements.txt

# ```

# 

# \### 5. Configure environment variables

# 

# Create a `.env` file in the project root:

# 

# ```env

# SECRET\_KEY=your-django-secret-key

# DEBUG=True

# ALLOWED\_HOSTS=127.0.0.1,localhost

# ```

# 

# Never upload your `.env` file or expose your secret key.

# 

# \### 6. Run database migrations

# 

# ```bash

# python manage.py migrate

# ```

# 

# \### 7. Start the development server

# 

# ```bash

# python manage.py runserver

# ```

# 

# Open http://127.0.0.1:8000/ in your browser.

# 

# \## Future Enhancements

# 

# \- Advanced student performance prediction.

# \- Improved personalized study recommendations.

# \- Expanded educational analytics.

# \- Enhanced AI-driven student support.

# 

# \## Project Purpose

# 

# neetEase demonstrates the practical application of web development, data analysis, and machine learning to an educational problem, with a focus on both academic performance and student well-being.



