import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# 1. Daten laden
# -----------------------------

df = pd.read_csv("data/owid-energy-data.csv")


# -----------------------------
# 2. Österreich auswählen
# -----------------------------

austria = df[df["country"] == "Austria"].copy()

# Nur Daten ab dem Jahr 2000
austria = austria[austria["year"] >= 2000]


# -----------------------------
# 3. Relevante Spalten auswählen
# -----------------------------

columns = [
    "country",
    "year",
    "population",
    "electricity_demand",
    "electricity_generation",
    "renewables_electricity",
    "renewables_share_elec",
    "fossil_electricity",
    "fossil_share_elec",
    "hydro_electricity",
    "wind_electricity",
    "solar_electricity"
]

austria = austria[columns]

# -----------------------------
# 4. Key Findings berechnen
# -----------------------------

# Daten ohne fehlende Werte für den Anteil erneuerbarer Energien
renewables = austria.dropna(subset=["renewables_share_elec"])

first_renewable = renewables.iloc[0]
latest_renewable = renewables.iloc[-1]

renewable_change = (
    latest_renewable["renewables_share_elec"]
    - first_renewable["renewables_share_elec"]
)

# Jahr mit dem höchsten Anteil erneuerbarer Energien
highest_renewable = renewables.loc[
    renewables["renewables_share_elec"].idxmax()
]

# Wind
wind = austria.dropna(subset=["wind_electricity"])

first_wind = wind.iloc[0]
latest_wind = wind.iloc[-1]

wind_change = (
    latest_wind["wind_electricity"]
    - first_wind["wind_electricity"]
)

# Solar
solar = austria.dropna(subset=["solar_electricity"])

first_solar = solar.iloc[0]
latest_solar = solar.iloc[-1]

solar_change = (
    latest_solar["solar_electricity"]
    - first_solar["solar_electricity"]
)


# Ergebnisse als Text vorbereiten
findings = [
    "--- Key Findings: Austria ---",
    "",
    f"Renewable electricity share:",
    f"{int(first_renewable['year'])}: "
    f"{first_renewable['renewables_share_elec']:.1f}%",
    f"{int(latest_renewable['year'])}: "
    f"{latest_renewable['renewables_share_elec']:.1f}%",
    f"Change: {renewable_change:+.1f} percentage points",
    "",
    f"Highest renewable electricity share:",
    f"{highest_renewable['renewables_share_elec']:.1f}% "
    f"in {int(highest_renewable['year'])}",
    "",
    f"Wind generation change:",
    f"{int(first_wind['year'])}: "
    f"{first_wind['wind_electricity']:.2f} TWh",
    f"{int(latest_wind['year'])}: "
    f"{latest_wind['wind_electricity']:.2f} TWh",
    f"Increase: {wind_change:.2f} TWh",
    "",
    f"Solar generation change:",
    f"{int(first_solar['year'])}: "
    f"{first_solar['solar_electricity']:.2f} TWh",
    f"{int(latest_solar['year'])}: "
    f"{latest_solar['solar_electricity']:.2f} TWh",
    f"Increase: {solar_change:.2f} TWh"
]


# In der Konsole ausgeben
for line in findings:
    print(line)


# Zusätzlich als Datei speichern
with open(
    "output/key_findings.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("\n".join(findings))

print(austria)


# -----------------------------
# 4. Diagramm:
# Erneuerbare vs. fossile Energie
# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    austria["year"],
    austria["renewables_share_elec"],
    label="Renewables"
)

plt.plot(
    austria["year"],
    austria["fossil_share_elec"],
    label="Fossil fuels"
)

plt.title("Electricity mix in Austria")
plt.xlabel("Year")
plt.ylabel("Share of electricity generation (%)")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/austria-electricity-mix.png"
)


# -----------------------------
# 5. Diagramm:
# Wasserkraft, Wind und Solar
# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    austria["year"],
    austria["hydro_electricity"],
    label="Hydropower"
)

plt.plot(
    austria["year"],
    austria["wind_electricity"],
    label="Wind"
)

plt.plot(
    austria["year"],
    austria["solar_electricity"],
    label="Solar"
)

plt.title("Renewable electricity generation in Austria")
plt.xlabel("Year")
plt.ylabel("Electricity generation (TWh)")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/austria-renewable-generation.png"
)

# -----------------------------
# 6. Vergleich:
# Österreich vs. Deutschland vs. EU
# -----------------------------

# Passende EU-Bezeichnung im Datensatz finden
available_countries = set(df["country"].dropna().unique())

eu_candidates = [
    "European Union (27)",
    "European Union (Ember)",
    "European Union"
]

eu_label = next(
    (country for country in eu_candidates if country in available_countries),
    None
)

if eu_label is None:
    possible_eu_labels = [
        country
        for country in available_countries
        if "European Union" in country
    ]

    raise ValueError(
        f"No EU aggregate found. Available EU labels: {possible_eu_labels}"
    )


# Vergleichsdaten auswählen
comparison = df[
    (df["country"].isin(["Austria", "Germany", eu_label]))
    & (df["year"] >= 2000)
][
    [
        "country",
        "year",
        "renewables_share_elec"
    ]
].dropna().copy()

# -----------------------------
# 7. Vergleichswerte berechnen
# -----------------------------

latest_common_year = comparison.groupby("country")["year"].max().min()

latest_comparison = comparison[
    comparison["year"] == latest_common_year
]

print(f"\n--- Country Comparison ({latest_common_year}) ---")

for _, row in latest_comparison.iterrows():

    display_name = row["country"]

    if display_name == eu_label:
        display_name = "European Union"

    print(
        f"{display_name}: "
        f"{row['renewables_share_elec']:.1f}%"
    )


# Werte separat holen
austria_value = latest_comparison.loc[
    latest_comparison["country"] == "Austria",
    "renewables_share_elec"
].iloc[0]

germany_value = latest_comparison.loc[
    latest_comparison["country"] == "Germany",
    "renewables_share_elec"
].iloc[0]

eu_value = latest_comparison.loc[
    latest_comparison["country"] == eu_label,
    "renewables_share_elec"
].iloc[0]


print(
    f"Austria vs Germany: "
    f"{austria_value - germany_value:+.1f} percentage points"
)

print(
    f"Austria vs EU: "
    f"{austria_value - eu_value:+.1f} percentage points"
)

# EU-Bezeichnung für das Diagramm vereinfachen
comparison["country"] = comparison["country"].replace(
    {eu_label: "European Union"}
)


# Diagramm erstellen
plt.figure(figsize=(10, 6))

for country in ["Austria", "Germany", "European Union"]:

    country_data = comparison[
        comparison["country"] == country
    ].sort_values("year")

    plt.plot(
        country_data["year"],
        country_data["renewables_share_elec"],
        label=country
    )


plt.title("Renewable electricity share: Austria vs Germany vs EU")
plt.xlabel("Year")
plt.ylabel("Share of electricity generation (%)")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/renewable-share-country-comparison.png"
)


# Alle drei Diagramme anzeigen
plt.show()