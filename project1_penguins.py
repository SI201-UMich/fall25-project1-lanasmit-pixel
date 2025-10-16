# Name: Lana Smith
# Email: lanasmith@umich.edu
# Collaborators: None
# AI Tools Used: ChatGPT (for structure and syntax help)
# Dataset: Palmer Penguins (Kaggle)

import csv

def load_csv(filename):
    """Reads the penguins.csv file into a list of dictionaries."""
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data


def calculate_average_body_mass_by_species(data):
    """Returns a dictionary of average body mass for each species."""
    species_totals = {}
    species_counts = {}

    for row in data:
        species = row["species"]
        mass_str = row["body_mass_g"]

        # skip missing or invalid values like "NA"
        if not mass_str or mass_str == "NA":
            continue

        body_mass = float(mass_str)
        species_totals[species] = species_totals.get(species, 0) + body_mass
        species_counts[species] = species_counts.get(species, 0) + 1

    avg_body_mass = {
        sp: species_totals[sp] / species_counts[sp]
        for sp in species_totals
    }
    return avg_body_mass


def calculate_above_avg_flipper_by_island(data):
    """Returns % of penguins with above-average flipper length by island."""
    flippers = [
        float(r["flipper_length_mm"]) for r in data
        if r["flipper_length_mm"] and r["flipper_length_mm"] != "NA"
    ]

    global_avg = sum(flippers) / len(flippers)

    island_counts = {}
    island_above = {}

    for row in data:
        flipper_str = row["flipper_length_mm"]
        if not flipper_str or flipper_str == "NA":
            continue

        island = row["island"]
        flipper = float(flipper_str)

        island_counts[island] = island_counts.get(island, 0) + 1
        if flipper > global_avg:
            island_above[island] = island_above.get(island, 0) + 1

    result = {
        i: round((island_above.get(i, 0) / island_counts[i]) * 100, 1)
        for i in island_counts
    }
    return result


def write_results_to_file(avg_mass, flipper_stats, output_file):
    """Writes results to a .txt file."""
    with open(output_file, "w") as f:
        f.write("Average Body Mass by Species:\n")
        for sp, val in avg_mass.items():
            f.write(f"{sp}: {round(val, 1)} g\n")

        f.write("\nPercentage of Penguins Above Avg Flipper Length by Island:\n")
        for island, pct in flipper_stats.items():
            f.write(f"{island}: {pct}%\n")


def main():
    data = load_csv("penguins.csv")
    avg_mass = calculate_average_body_mass_by_species(data)
    flipper_stats = calculate_above_avg_flipper_by_island(data)
    write_results_to_file(avg_mass, flipper_stats, "penguin_results.txt")

    print("✅ Results written to penguin_results.txt")


if __name__ == "__main__":
    main()
