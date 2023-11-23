
# Football Manager 2024 Svonnalytics Dashboard

*Für eine deutsche Version dieser Anleitung, siehe [LIESMICH.md](LIESMICH.md).*

## What is this about?
Welcome to the Scouting & Analytics Dashboard for Football Manager 2024, developed by me, Svonn. This tool was designed for "Veni Vidi Vici", an online multiplayer save game with over 30 human trainers. It calculates an overall score for players based on key attributes relevant to their roles. Further details on how scores are calculated are provided below. Currently, this dashboard is compatible with the German version of the game (23/24), with an English version coming soon. Currently, it requires all attributes to be revealed, which is usually the case in multiplayer saves, as players do not have time to manage their scouts between games.

![Dashboard Screenshot](images/showcase.jpg)

## Installing, Starting, and Stopping

### Installation
1. **Clone the Repository**: 
   - If you're familiar with Git, clone this repository using your preferred method.
   - For those new to this, follow these steps:
     - Download and install Git from [git-scm.com](https://git-scm.com/downloads).
     - Open Git Bash and type `git clone [repository link]`.
2. **Download as ZIP**: 
   - Alternatively, you can download this repository as a ZIP file.
   - Unzip the file to your desired location on your computer.

### Starting the Dashboard
- Run `svonnalytics_dashboard.bat`.
- This will automatically install all necessary software dependencies and start the dashboard.
- During the startup, you'll be prompted to enter a path for where you want to keep your player data. You can use the default or specify your own.

### Stopping the Dashboard
- To close the program, press `Ctrl+C` in the console or simply close the console window.

## Loading Data

1. **In Football Manager 2024**:
   - Go to the scouting tab.
   - Right-click the columns and select "Import view".
   - Import the view named `svonnalytics_view.fmf` located in `views_and_filters/`.

2. **Filtering Players**:
   - For our multiplayer game "Veni Vidi Vici", use the filter `vvv_relevant_players_filter.fmf` in `views_and_filters/`. This filters out irrelevant players based on league participation and squad status.
   - When scouting for players I'd recommend clicking the filter "Interested in Transfers" or "Interested in Loans". If that doesn't remove enough players (Still >5000), then I'd recommend filtering by something like adding all stats -> require 15 -> at least 7/x match. Adjust this depending on your teams league, status etc.

3. **Exporting Players**:
   - Select the players you wish to export (use `Ctrl+A` for all).
   - Press `Ctrl+P` and export them as a website/html file to the output directory you have selected during startup (default is `%USERPROFILE%\Documents\Sports Interactive\Football Manager 2024\exported_html`).

4. **Using the Dashboard**:
   - Once the HTML file is ready, you can select it at the top of the dashboard.

> [!IMPORTANT]  
> * To include your own players, go to the filter menu, select "exclude", and uncheck "YOUR CLUB - Players".
> * If the dashboard fails to load the HTML, ensure you have selected the correct view. If issues persist, check the exported HTML for empty rows - a known issue in FM, try to reduce the amount of exported players.

## Limitations

Remember, Football Manager is a complex game and success depends on various factors. This tool offers insights but cannot fully capture the game's nuances.

## Customizing

- You can adjust attribute weightings and displayed stats for each role in `configurations.py`.
- To add a new role, follow these steps:
  - Add an entry in `role_attributes` in `configurations.py`.
  - If applicable, add the left/right mapping below (like for other wingers).
  - Add the role to `role_mapping` with relevant positions.
- Save the file - the role should now appear in your dashboard.

## Dashboard Tabs Overview

### Default Screen
- **Description**: This screen displays all players sorted by their best role score, irrespective of whether they can actually play that role. It includes scores for each role and additional player information.
- ![Default Screen Screenshot](images/overview.jpg)

### Role -> Player
- **Description**: This tab shows all exported players capable of playing the selected role. It provides the role score along with relevant statistics.
- ![Role -> Player Screenshot](images/players.jpg)

### Role -> Club Averages
- **Description**: Displays the average scores for each role across all players in a club. Useful for getting a general idea of a club's strengths in specific roles.
- ![Role -> Club Averages Screenshot](images/club_averages.jpg)

### Role -> Club Best
- **Description**: Shows the best score for a specific role within each club, highlighting the top performer in each role.
- ![Role -> Club Best Screenshot](images/club_best.jpg)

### Role -> League Averages
- **Description**: This tab presents the average scores for each role across the entire league, offering insights into league-wide trends and standards.
- ![Role -> League Averages Screenshot](images/league_averages.jpg)

### Role -> League Best
- **Description**: Displays the average of the best scores for each club in the league for a particular role, showcasing top talent in each role across the league.
- ![Role -> League Best Screenshot](images/league_best.jpg)

### Aggregated -> Club Overall Scores
- **Description**: Shows the average of "Club Average" scores for each role, giving an overview of a club's overall strength in various roles.
- ![Aggregated -> Club Overall Scores Screenshot](images/aggregated_club_overall.jpg)

### Aggregated -> Club Max Scores
- **Description**: This tab displays the average of the "Club Best" scores for each role, indicating the peak performance levels within a club.
- ![Aggregated -> Club Max Scores Screenshot](images/aggregated_club_max.jpg)

### Aggregated -> League Overall Scores
- **Description**: Presents league-wide averages for each role, allowing you to compare overall role strengths across the league.
- ![Aggregated -> League Overall Scores Screenshot](images/aggregated_league_overall.jpg)

### Aggregated -> League Max Scores
- **Description**: Shows the average of the best scores for each role across all clubs in the league, which should roughly resemble the average best starting eleven in a league.
- ![Aggregated -> League Max Scores Screenshot](images/aggregated_league_max.jpg)


I hope my tool helps improving your enjoyment of Football Manager.