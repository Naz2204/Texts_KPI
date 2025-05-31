# Installation
## Creating virtual environment
* ### Open folder where API files must be located
* ### Create *__.venv__* by executing command below
```
python -m venv .venv
```
* ### Activate virtual environment via running next command
**cmd**
```
.venv\Scripts\activate
```
**powershell**
```
.\.venv\Scripts\Activate.ps1
```
**bash**
```
source .venv\Scripts\activate
```
## Installing libraries
After activating virtual environment install needed libs
Simply run the following command using *__requirements.txt__*
```
pip install -r requirements.txt
```

## Starting up server
Just run *__main.py__* or the following command
```
granian --interface asgi API:app
```
Add *__--reload__* at the end in case you need autoreload after code changes