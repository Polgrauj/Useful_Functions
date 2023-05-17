# Useful Functions

This folder contains different functions useful to be used either for ML algorithms, data cleaning, result representation..., all of them detailed below.

1. Heatmap analysis plot. Prints a heatmap of statistical analyses such as Chi-2, Z-score, P-values, etc; of cluster/group-wise analyses. Takes as input a dataframe containing the groups-wise analyses on the columns and the variables analysed on the rows, the name of the variables analysed as a list of strings and the number of groups compared (it is supposed that is a group-wise analysis and therefore for e.g., 4 groups, there are 6 combinations [0-1, 0-2, 0-3, 1-2, 1-3, 2-3], considered bidirectional). Other parameters regarding the plot outcomes can be defined as input variables.
