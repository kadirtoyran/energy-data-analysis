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


# Beide Diagramme anzeigen
plt.show()