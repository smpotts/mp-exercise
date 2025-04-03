import json
import csv
import pandas as pd
import matplotlib.pyplot as plt


def consume_raw_proficiency_file():
    with open("data/proficiency.json", "r") as file:
        try:
            raw_profs = json.load(file)
            cleaned_vals_list = []
            for value in raw_profs['proficiency']:
                if value is not None and isinstance(value, int):
                   cleaned_vals_list 
            return cleaned_vals_list
        except Exception:
            print("Error reading 'proficiency.json' file.")


def consume_raw_skills_file():
    with open("data/skills.json", "r") as file:
        try:
            raw_skills = json.load(file)
            cleaned_records_list = []
            for record in raw_skills['skills']:
                skill = record.get('skill')
                # make sure the skill key is in the record and it's just one char
                if skill is not None and isinstance(skill, str) and len(skill) == 1:
                    cleaned_records_list.append(record)
            return cleaned_records_list
        except Exception:
            print("Error reading 'skills.json' file.")


def consume_raw_data_file():
    with open("data/data.json", "r") as file:
        try:
            data = json.load(file) 
            cleaned_records_list = []

            for record in data['scores']:   
                skill = record.get("skill")
                score = record.get("score")

                # checking to make sure both keys exist in a record
                if skill is not None and score is not None:
                    # making sure the values match
                    # TODO: there is a value that is a double, should we cast this to an integer and keep is or is it bad data?
                    if isinstance(skill, str) and len(skill) == 1 and isinstance(score, int):
                        cleaned_records_list.append(record)
            
            return cleaned_records_list
           
        except Exception :
            print("Error reading 'data.json' file.")

def output_timeseries(data):
    # TODO: unclear how to make the data timeseries without a timestamp, so ordering by skill then score since that's what we have
    # TODO: requirements say CSV and then reference JSON file name "(time-series.json)", so making it a csv
    sorted_data = sorted(data, key=lambda x: (x["skill"], x["score"]))
    
    with open("data/time-series.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["skill", "score"]) # headers
        for record in sorted_data:
            writer.writerow([record["skill"], record["score"]])


def calculate_skill_analytics(data):
    df = pd.DataFrame(data)
    # we convert that index into a regular column and make it a proper DataFrame with two named columns
    skill_counts = df["skill"].value_counts().reset_index()
    skill_counts.columns = ["skill", "count"]

    # now calculate average scores
    average_scores = df.groupby("skill")["score"].mean().reset_index()
    
    # merge the average score into the skill_counts DataFrame
    result = pd.merge(skill_counts, average_scores, on="skill", how="left")
    result = result.rename(columns={"score": "proficiency"})
    
    # TODO: no file name provided in the instructions so making one up
    result.to_csv("data/proficiency_by_skill.csv")

    return result


def visualize(df):
    # plot a bar chart for 'count' and 'average_score' side by side
    df.set_index('skill')[['count', 'proficiency']].plot(kind='bar', figsize=(8, 6))

    # set the labels and title
    plt.xlabel('Skill')
    plt.ylabel('Values')
    plt.title('Skill Count and Average Proficiency')

    # show the plot
    plt.show()


def process():
    cleaned_data = consume_raw_data_file()
    output_timeseries(cleaned_data)    
    consume_raw_skills_file()
    consume_raw_proficiency_file()

    results = calculate_skill_analytics(cleaned_data)
    visualize(results)


if __name__ == "__main__":
    process()

