# Word Search Puzzle Generator
##### Generate a 20 X 20 printable word search puzzle and answer key based on user input. The project is deployed [here](https://word-search-puzzle.herokuapp.com).

### File Structure

This project utilizes the Flask web framework and has been deployed with gunicorn and heroku.  All dependencies can be found in requirements.txt. HTML templates and CSS are in the templates and static folders, respectively. All app logic is located in app.py.

### Customization 
##### Grid Size

Grid size is determined by the global variable size. Change this variable for smaller/bigger puzzles. **Note: changing the size of the puzzle may affect print formatting.**

##### Patterns and Word Placement
The puzzle generator currently supports word placement:
  * horizontally(forward)
  * horizontally(backward)
  * vertically(top to bottom)
  * vertically(bottom to top)
  * diagonally(top-left to bottom-right)
  * diagonally(bottom-left to top-right)
  
Patterns can be enabled/disabled by creating a new function and including it or removing it from the placement_functions list in the randomizer function. Additionally, the weighted algorithm can be modified by changing any of the constant weight-values in the list.

### Author 
[Josef Goodyear](https://github.com/JosefGoodyear)
