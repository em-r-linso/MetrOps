# MetrOps

## Description

This web app is a tool for running and playing the game of the same name.

MetrOps is roleplaying game of my own design.

Built with [Django](https://www.djangoproject.com/).

## Installation

### Prerequisites

- Python 3.12.1 (not tested on other versions)

### Setup

1. Clone this repo:

    Windows:

    ```bash
    git clone https://github.com/em-r-linso/MetrOps.git
    cd MetrOps
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    ```

    macOS/Linux:

    ```bash
    git clone https://github.com/em-r-linso/MetrOps.git
    cd MetrOps
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    ```

2. Generate a secret key:

    ```bash
    python -m django.core.management.utils.get_random_secret_key
    ```

3. Create `.env` in the root directory and add the following:

    ```plaintext
    DJANGO_SECRET_KEY=your_secret_key
    DEBUG=True
    ```

## Usage

### Running the App

1. If the virtual environment is not already activated, activate it:

    Windows:

    ```bash
    .\venv\Scripts\activate
    ```

    macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

2. Run the server:

    ```bash
    python manage.py runserver
    ```

The app will run at localhost:8000.

### Admin

You will need to populate the database yourself by creating a user and logging in to the admin panel.

```bash
python manage.py createsuperuser
```

The admin panel is accessible at localhost:8000/admin.

### Database

This app uses SQLite, so you don't need to set up a database server.

Any changes to the models will require a migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Contribution

Pull requests and issues are welcome.