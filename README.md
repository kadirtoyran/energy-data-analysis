# Austria Energy Data Analysis

This project analyzes the development of Austria's electricity mix since 2000 using publicly available energy data from Our World in Data.

The goal is to explore how renewable and fossil electricity generation have changed over time and to visualize the development of hydropower, wind and solar energy.

## Technologies

- Python
- pandas
- matplotlib
- Git
- GitHub

## Data

The project uses the Our World in Data Energy Dataset.

The analysis focuses on Austria and uses data from the year 2000 onwards.

## Analysis

The project currently examines:

- renewable vs. fossil electricity generation
- renewable electricity share
- hydropower generation
- wind power generation
- solar power generation

## Visualizations

### Renewable vs. fossil electricity

![Austria electricity mix](output/austria-electricity-mix.png)

### Renewable electricity generation

![Austria renewable generation](output/austria-renewable-generation.png)

## Project Structure

```text
energy-data-analysis/
├── data/
│   └── owid-energy-data.csv
├── output/
│   ├── austria-electricity-mix.png
│   └── austria-renewable-generation.png
├── src/
│   └── analysis.py
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/kadirtoyran/energy-data-analysis.git
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python src/analysis.py
```

## Next Steps

Planned improvements include:

- calculating key statistics automatically
- comparing Austria with other European countries
- analyzing long-term trends
- adding further visualizations