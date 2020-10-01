# CricLive Score

## Setup instructions

- Python3 must be installed.

- The app has been only tested on MacOS.

- Execute the following in the project root folder. You must replace the location of `.bash_profile` with the exact location in your system.
```
pip install -r requirements.txt

aa=$PWD;echo 'alias criclive="python '$aa'/criclive.py"' >> ~/.bash_profile
source ~/.bash_profile
```

## Testing the app

- Test the app by executing the following.
```
criclive -h
criclive
```

- If the app cannot find Python3, replace line 1 in `criclive.py` with the actual path to Python3 in your system.
