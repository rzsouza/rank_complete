# rank_complete

Calculates the transitive ranking for teams.

Example:
If Italy wins vs France and France wins vs Germany, Italy gets the points for winning against Germany

Rules to calculate the ranking:
1) All points for games played are added up
2) Transitive points are added up following the shortest valid path between 2 teams
3) If no valid path can be found, each team is awarded a draw (1 point)

Valid path is any path that links two teams with a valid sequence of results that leads to a natural result. For example:
Valid: Ita 1 x 0 Fra -> Fra 1 x 0 Ger conclusion: Italy wins vs Germany
Valid: Ita 1 x 0 Fra -> Fra 0 x 0 Ger conclusion: Italy wins vs Germany
Invalid: Ita 1 x 0 Fra -> Fra 0 x 1 Ger conclusion: No logical conclusion about the result of Italy vs Germany
