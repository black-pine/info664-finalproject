## Pratt Info-664 Programming for Cultural Heritage
This repository contains the files for the final project for PFCH, completed in the Spring 2021 semester.  This project is focused around the comic book industry and single issue sales data.\
\
To re-use this project code, an API key is required for both the Marvel API (marvelAPI.py) and Twitter API (randomizeTweet.py).  There also must be two folders in the same directory as the project files: a "records" folder in order to save the Marvel API .JSON files (marvelAPI.py) and an "images" folder in order to locally save images from URLs in the Marvel API to use for Twitter (randomizeTweet.py).  The order to run the files is: webScrapeMayo.py, calculateStats.py, calculateMarvel.py, marvelAPI.py, globMarvel.py, randomizeTweet.py.  This project will create .CSV, .JSON, .XLSX, and image (typically .JPG) files.
\
\
Data visualizations based on this data can be found on Tableau: https://public.tableau.com/profile/sumi3573#!/vizhome/PFCH-comics/RevxPub \
Twitter integration can be found @pfch_marvel: https://twitter.com/pfch_marvel \
Project and findings summary can be found on my personal website: https://sumi.matsumoto.com/pratt/pfch