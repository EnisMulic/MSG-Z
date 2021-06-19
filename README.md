# MSG-Z

## Running the application

#### Clone the repository and navigate to the application

```
git clone https://github.com/EnisMulic/MSG-Z.git
cd MSG-Z
```

#### Create an environment file with your settings

```
cp example.env .env
```

#### Install the python virtual environment

```
pip install pipenv
```

#### Start the virtual environment

```
pipenv shell
```

#### Install dependencies

```
pipenv install
```

#### Start the application

```
python bot.py
```

## Updating the database

```
alembic revision --autogenerate -m "<Message>"
alembic upgrade head
```
