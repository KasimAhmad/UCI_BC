import os
import csv 
total_votes = 0
candidate = {}
candidate_options = []
candidate_percentage = []
winning_vote_count = 0
winner = 0

csvpath = os.path.join("Resources", "election_data.csv")
with open(csvpath) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    print(csvreader)
    csv_header = next(csvreader)
    print(f'CSV Header: {csv_header}')
    for row in (csvreader):
        total_votes = total_votes + 1
        candidate_name = row[2]
        if candidate_name not in candidate_options:
            candidate_options.append(candidate_name)
            candidate[candidate_name] = 1
        else:
            candidate[candidate_name] += 1
for unique_voter in candidate_options:
    candidate_percentage.append(round(candidate[unique_voter] / total_votes * 100, 2))
    if candidate[unique_voter] > winning_vote_count:
        winning_vote_count = candidate[unique_voter]
        winner = unique_voter

summary = (f"""\nVoter Analysis\n
    ----------------------------\n
    Total number of votes: {total_votes}\n
     ----------------------------\n
    Khan: {candidate_percentage[0]:.3f}% ({candidate["Khan"]})
    Correy: {candidate_percentage[1]:.3f}% ({candidate["Correy"]})
    Li: {candidate_percentage[2]:.3f}% ({candidate["Li"]})
    O'Tooley: {candidate_percentage[1]:.3f}% ({candidate["O'Tooley"]})\n
    Winner: {winner}""")

print(summary)

# Export
export_name = os.path.join("Analysis", "election_analysis.txt")
with open(export_name, "a") as txt:
    txt.write(summary)
