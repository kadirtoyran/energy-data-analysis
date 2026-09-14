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